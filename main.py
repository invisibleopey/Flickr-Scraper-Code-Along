from scrapper import get_urls
import dtlpy as dl

if dl.token_expired():
    dl.login()

project = dl.projects.get(project_name='Custom Vision Model')

urls = get_urls()

for url_dict in urls:
    for key in url_dict:
        dataset = project.datasets.create(dataset_name=key)
        dataset.add_label(label_name=key)
        for val in url_dict[key]:
            url_path = val
            # Create link
            link = dl.UrlLink(ref=url_path, mimetype='image')
            # Upload link
            item = dataset.items.upload(local_path=link)
