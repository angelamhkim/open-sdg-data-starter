# -*- coding: utf-8 -*-
"""
This script makes several tweaks to the metadata to migrate it into the new
platform.

"""

import glob
import os.path
import frontmatter

# For more readable code below.
FOLDER_META = 'meta'

def update_metadata(indicator):

    with open(indicator, 'r') as f:
        post = frontmatter.load(f)

        # Figure out the graph_type and data_non_statistical.
        data_non_statistical = False
        graph_type = 'line'
        if 'graph' not in post.metadata or post['graph'] == None or post['graph'] == '':
            graph_type = None
            data_non_statistical = True
        elif post['graph'] == 'bar':
            graph_type = 'bar'
        elif post['graph'] == 'binary':
            graph_type = 'binary'
        post.metadata['data_non_statistical'] = data_non_statistical
        post.metadata['graph_type'] = graph_type
        # Clean up the unused variable.
        if 'graph' in post.metadata:
            del post.metadata['graph']

    with open(indicator, 'w') as f:
        f.write(frontmatter.dumps(post))

    return post

def main():
    """Update all all of the indicators in the metadata folder."""

    status = True

    # Read all the files in the source location.
    indicators = glob.glob(FOLDER_META + "/*.md")
    print("Attempting to update " + str(len(indicators)) + " metadata files...")

    # Compile all the possible metdata keys.
    all_keys = {}

    for indicator in indicators:
        result = update_metadata(indicator)
        if result:
            for key in result.metadata:
                all_keys[key] = True
        status = status & (result != None)

    #for key in all_keys.keys():
    #    print(key)

    return status

if __name__ == '__main__':
    if not main():
        raise RuntimeError("Failed to migrate metadata")
    else:
        print("Success")
