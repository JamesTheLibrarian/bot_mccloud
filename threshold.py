import os
import subprocess

for page_path in os.listdir('./raw'):
    # skip anything that isn't a PNG file
    if page_path[-4:] != '.png':
        continue

    # use ImageMagick to threshold each page
    thresholded_path = './thresholded/' + page_path
    raw_path = './raw/' + page_path
    subprocess.call(['convert', raw_path, '-type', 'Grayscale', '-white-threshold', '50%', thresholded_path])
    print 'Thresholding ' + page_path + '...'
print 'Done.'
