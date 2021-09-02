#!/usr/bin/env python
# coding: utf-8

import argparse
import json
import logging
import os
import shutil

from jinja2 import Environment, FileSystemLoader
from markdown import markdown

parser = argparse.ArgumentParser()
parser.add_argument('-i', dest='sources_folder', help='HTML input sources folder')
parser.add_argument('-s', dest='less_sources_folder', help='LESS input sources folder')
parser.add_argument('-t', dest='page_title', nargs='+', default='', help='Optional page title')
parser.add_argument('-o', dest='build_folder', help='Build directory')
parser.add_argument('-v', dest='valuefile', help='File path to a file containing JSON data, handed over to the context')
args = parser.parse_args()

logging.basicConfig(format='[%(levelname)s] HTML renderer: %(message)s')
logger = logging.getLogger('renderer')
logger.setLevel('INFO')


if not all([args.sources_folder, args.build_folder]):
    raise Exception('Missing arguments. Need sources_folder and build_folder')


html_sources_folder = os.path.join(args.sources_folder, 'jinja')
less_sources_folder = os.path.join(args.sources_folder, 'less')
static_sources_folder = os.path.join(args.sources_folder, 'static')
build_folder = args.build_folder
static_folder = os.path.join(build_folder, 'static')
page_title = ' '.join(args.page_title)

values = None
if args.valuefile:
    with open(args.valuefile) as f:
        values = json.loads(f.read())


if not os.path.exists(build_folder):
    logger.info('Creating directory: %s', build_folder)
    os.makedirs(build_folder)

if not os.path.exists(os.path.join(build_folder, 'styles')):
    logger.info('Creating directory: %s', os.path.join(build_folder, 'styles'))
    os.makedirs(os.path.join(build_folder, 'styles'))

if not os.path.exists(static_folder):
    logger.info('Creating directory: %s', static_folder)
    os.makedirs(static_folder)

logger.info('Copying static files')
if os.path.exists(static_folder):
    shutil.rmtree(static_folder)

try:
    shutil.copytree(static_sources_folder, static_folder)
except OSError:
    logger.info("No static files found.")

env = Environment(loader=FileSystemLoader(os.path.abspath(html_sources_folder)))
env.filters['markdown'] = markdown


def create_subdirs():
    for root, dirs, filenames in os.walk(html_sources_folder):
        for dirname in dirs:
            path = os.path.join(build_folder, dirname)
            logger.info('Creating directory: %s', path)
            os.makedirs(path)


def get_html_source_files():
    files = []
    for root, dirs, filenames in os.walk(html_sources_folder):
        for filename in filenames:
            if not filename.startswith('_') and filename.endswith('.jinja'):
                files.append(os.path.join(os.path.relpath(root, html_sources_folder), filename))
    return files


def get_css_source_files():
    files = []
    for root, dirs, filenames in os.walk(less_sources_folder):
        for filename in filenames:
            files.append(filename)
    return files


def get_static_files():
    files = []
    for root, dirs, filenames in os.walk(static_folder):
        for filename in filenames:
            rel_dir = os.path.relpath(root, static_folder)
            files.append(os.path.join(rel_dir, filename).lstrip('./'))
    return files


def url_for(name):
    urls = {}
    for jinja_file in get_html_source_files():
        jinja_file = jinja_file.replace('jinja', 'html').replace('./', '')
        urls[jinja_file] = jinja_file
    for less_file in get_css_source_files():
        less_file = less_file.replace('less', 'css')
        urls[less_file] = 'styles/' + less_file
    for static_file in get_static_files():
        urls[static_file] = 'static/' + static_file
    return urls[name]


def render_file(template_name):
    logger.info('Rendering HTML template {}'.format(template_name))
    context = {}
    context['title'] = page_title
    logger.info('Using page title: {}'.format(page_title))
    context['url_for'] = url_for
    if values:
        context.update(values)
    template = env.get_template(template_name)
    template.stream(context).dump(os.path.join(build_folder, template_name.replace('jinja', 'html')))


logger.info('Start rendering HTML')
logger.info('Using HTML sourcess: %s, less sources: %s, build directory: %s',
            html_sources_folder, less_sources_folder, build_folder)

if not get_html_source_files():
    logger.error('No input files found')

create_subdirs()

for filename in get_html_source_files():
    render_file(filename)
