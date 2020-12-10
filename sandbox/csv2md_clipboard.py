import subprocess
import csv
import io
import pandas.io.clipboard

def md_to_html(md):
  return subprocess.check_output(["pandoc", '-f', 'markdown', '-t', 'html'], input=md.encode('utf-8')).decode('utf-8')

def text_cells_from_clipboard():
  clipboard = io.StringIO(pandas.io.clipboard.clipboard_get())
  return [x[0] for x in csv.reader(clipboard)]

def clipboard_to_html():
  md = '\n\n'.join(text_cells_from_clipboard())
  md = md.replace('\n# ', '\n## ')
  html = md_to_html(md)
  pandas.io.clipboard.clipboard_set(html)
  
