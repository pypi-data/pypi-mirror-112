from mkdocs.plugins import BasePlugin
from mkdocs.config.config_options import Type

import jinja2
from pathlib import Path

class ExportPlugin(BasePlugin):
    """
    Creates "export.json" file containing all docs using the template
    """

    config_scheme = (
        ('export_folder', Type(str, default='')),
        ('export_filename', Type(str, default='docs.json')),
        ('export_template', Type(str))
    )

    def __init__(self):
        self.docsData = []
        self.export_filename = "docs.json"
        self.export_folder = ""
        self.export_template = None

    def on_config(self, config):
        self.export_filename = Path(self.config.get("export_filename") or self.export_filename)
        self.export_folder = Path(self.config.get("export_folder") or config["site_dir"])
        if not self.export_folder.is_absolute():
            self.export_folder = Path(config["docs_dir"]) / ".." / self.export_folder
        if not self.export_folder.exists():
            self.export_folder.mkdir(parents=True)

        if self.config.get("export_template"):
            self.export_template = Path(self.config.get("export_template"))

    def on_page_markdown(self, markdown, **kwargs):
        page = kwargs.get('page')
        self.docsData.append(page)
        return markdown

    def on_post_build(self, config):
        if self.export_template is None:
            templ_path = Path(__file__).parent  / Path("templates")
            environment = jinja2.Environment(
                loader=jinja2.FileSystemLoader(str(templ_path))
                )
            templ = environment.get_template("export.json.template")
        else:
            environment = jinja2.Environment(
                loader=jinja2.FileSystemLoader(searchpath=str(self.export_template.parent))
            )
            templ = environment.get_template(str(self.export_template.name))
        output_text = templ.render(
                pages=self.docsData,
        )

        with open(str(self.export_folder / self.export_filename), "w") as f:
            f.write(output_text)