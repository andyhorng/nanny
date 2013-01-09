# coding: utf-8
import os
import shutil
import tempfile
import subprocess
import yaml
import pystache

TEMPLATES = os.path.expanduser("~/templates/")

class Scanner(object):
    def __init__(self, template, templates=TEMPLATES):
        self.templates = templates
        self.template = template

    def fetch_variables(self, path):
        # text to be render
        text = open(os.path.join(self.templates, self.template, path), 'r').read()
        text = text + path
        parsed = pystache.parser.parse(unicode(text))

        # TODO: scan folder/file names
        def has_key(item):
            return hasattr(item, 'key')
        # remove duplicated
        return list(set([node.key for node in filter(has_key, parsed._parse_tree)]))

    def _scan(self, prefix, d):
        """
        scan variables recursively
        """
        basepath = os.path.join(prefix, d)

        dirs = os.listdir(basepath)
        result = []
        for item in dirs:
            path = os.path.join(basepath, item)
            if os.path.isdir(path):
                result = result + self._scan(basepath, item)
            else:
                result = result + self.fetch_variables(path)

        return list(set(result))

    def scan(self):
        return self._scan(os.path.join(self.templates, self.template), "")


class Templater(object):
    def __init__(self, template, templates=TEMPLATES):
        self.template = template
        self.templates = templates
        self.desc_path = os.path.join(templates, template, "description.yml")
        self.dynamic_path = os.path.join(templates, template, "description.py")

    def render_yaml(self, scan_result):
        result = dict()
        # load original
        if os.path.isfile(self.desc_path):
            original = yaml.safe_load(open(self.desc_path))
            if isinstance(original, dict):
                result = original

        for var in scan_result:
            if var not in result:
                result[var] = {
                    "example": "",
                    "description": ""
                    }
        return yaml.safe_dump(result, default_flow_style=False)

    def write_yaml(self, scan_result, path):
        result = self.render_yaml(scan_result)
        with open(path, 'w') as f:
            f.write(result)

    def build_template(self):
        scanner = Scanner(template=self.template,
                          templates=self.templates)
        self.write_yaml(scanner.scan(), self.desc_path)


class Builder(object):
    def __init__(self, template, templates=TEMPLATES):
        self.template = template
        self.templates = templates
        self.description = yaml.safe_load(open(os.path.join(templates,
                                                       template,
                                                       "description.yml")))
        self.dynamic_path = os.path.join(templates, template, "dynamic.py")

    def load_dynamic(self, context):
        with open(self.dynamic_path) as script:
            exec script in context
        return context

    def build(self):
        # fill
        with tempfile.NamedTemporaryFile() as f:
            config = dict()
            for key, value in self.description.items():
                config[key] = value['example']
            yaml.safe_dump(config, f, default_flow_style=False)
            subprocess.call(["vim", f.name])
            context = yaml.safe_load(open(f.name))
            self.build_final(self.load_dynamic(context))

    def build_final(self, context, dest=os.getcwd()):
        import shlex
        path = os.path.join(self.templates, self.template)
        paths = " ".join(os.path.join(path, item) for item in os.listdir(path))
        command = "rsync -av %s %s" % (paths, dest)
        subprocess.check_call(shlex.split(command))

        # render content
        for root, dirs, files in os.walk(dest):
            if files:
                for name in files:
                    with open(os.path.join(root, name), 'r+') as f:
                        print "rendering %s ..." % os.path.join(root, name)
                        template = f.read().decode('UTF-8')
                        f.seek(0)
                        f.truncate()
                        f.write(pystache.render(template, context))

        # folder names
        for root, dirs, files in os.walk(dest):
            if dirs:
                for dir_ in map(lambda i: os.path.join(root, i), dirs):
                    parsed = pystache.parser.parse(unicode(dir_))
                    if any(hasattr(item, 'key') for item in parsed._parse_tree):
                        new_dir = os.path.join(root, pystache.render(dir_, context))
                        if not os.path.exists(new_dir):
                            os.makedirs(new_dir)
                        for template in os.listdir(dir_):
                            shutil.copy(os.path.join(dir_, template), new_dir)
                        shutil.rmtree(dir_)

        # file names
        for root, dirs, files in os.walk(dest):
            if files:
                for f in map(lambda i: os.path.join(root, i), files):
                    parsed = pystache.parser.parse(unicode(f))
                    if any(hasattr(item, 'key') for item in parsed._parse_tree):
                        # rename
                        os.rename(f, pystache.render(parsed, context))
