import os
from PIL import Image


def find_row_bounds(image, (min_x, min_y, max_x, max_y)):
    rows = []
    row = None
    for y in range(min_y, max_y):
        row_is_allwhite = True
        for x in range(min_x, max_x):
            pixel = image.getpixel((x, y))
            if pixel != 255 and pixel != (255, 255, 255, 255):
                row_is_allwhite = False
                break
        if row_is_allwhite:
            # finish up the current panel row if it exists
            if row:
                rows.append(row)
                row = None
        else:
            # add this row of pixels to the existing panel row, or a new panel row if none exists
            row = (row[0], y) if row else (y, y)
    if row:
        rows.append(row)

    # discard panel rows that are less than 30px high
    rows = list(filter(lambda (start, end): end - start >= 30, rows))

    panel_bounds = []
    if len(rows) > 1:
        for (start_y, end_y) in rows:
            panel_bounds.extend(find_col_bounds(image, (min_x, start_y, max_x, end_y)))
    elif len(rows) == 0:
        panel_bounds.append((min_x, min_y, max_x, max_y))
    else:
        panel_bounds.append((min_x, rows[0][0], max_x, rows[0][1]))
    return panel_bounds


def find_col_bounds(image, (min_x, min_y, max_x, max_y)):
    cols = []
    col = None
    for x in range(min_x, max_x):
        col_is_allwhite = True
        for y in range(min_y, max_y):
            pixel = image.getpixel((x, y))
            if pixel != 255 and pixel != (255, 255, 255) and pixel != (255, 255, 255, 255):
                col_is_allwhite = False
                break
        if col_is_allwhite:
            # finish up the current panel col if it exists
            if col:
                cols.append(col)
                col = None
        else:
            # add this col of pixels to the existing panel col, or a new panel col if none exists
            col = (col[0], x) if col else (x, x)
    if col:
        cols.append(col)

    # discard panel cols that are less than 10px wide
    cols = list(filter(lambda (start, end): end - start >= 10, cols))

    panel_bounds = []
    if len(cols) > 1:
        for (start_x, end_x) in cols:
            panel_bounds.extend(find_row_bounds(image, (start_x, min_y, end_x, max_y)))
    elif len(cols) == 0:
        panel_bounds.append((min_x, min_y, max_x, max_y))
    else:
        panel_bounds.append((cols[0][0], min_y, cols[0][1], max_y))
    return panel_bounds


def find_panel_bounds(image):
    bounds_1 = find_row_bounds(image, (0, 0, image.width, image.height))
    bounds_2 = find_col_bounds(image, (0, 0, image.width, image.height))
    bounds = bounds_2 if len(bounds_2) > len(bounds_1) else bounds_1
    # discard "panels" smaller than 100px in either dimension (they're probably erroneous)
    new_bounds = filter(lambda (x1, y1, x2, y2): x2 - x1 >= 100 and y2 - y1 >= 100, bounds)
    if len(new_bounds) < len(bounds):
        print 'Discarded ' + str(len(bounds) - len(new_bounds)) + ' panels for being too small!'
    return new_bounds


def panelize(page_path):
    # use the thresholded version of the page to find panel bounds
    with Image.open('./thresholded/' + page_path) as thresholded:
        thresholded = thresholded.convert('L')
        panel_bounds = find_panel_bounds(thresholded)
        print 'Found ' + str(len(panel_bounds)) + ' panels!'

    # crop the panels out of the raw version of the page and save them to the panels dir
    with Image.open('./raw/' + page_path) as page:
        for panel_id, bounds in enumerate(panel_bounds):
            panel = page.crop(bounds)
            panel.save('./panels/' + page_path[:-4] + ' ' + str(panel_id) + '.png')


for page_path in os.listdir('./raw'):
    # skip anything that isn't a PNG file
    if page_path[-4:] != '.png':
        continue
    print 'Panelizing ' + page_path + '...'
    panelize(page_path)
    print '---'
print 'Done.'
