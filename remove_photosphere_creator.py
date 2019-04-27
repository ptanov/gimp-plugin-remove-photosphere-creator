 #!/usr/bin/env python

from gimpfu import *
import datetime

DEFAULT_HEIGHT = 600
STEP = 100

def remove_photosphere_creator_batch(pattern, destination_folder, height = DEFAULT_HEIGHT):
    import glob
    import os
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    success = 0
    errors = []
    before_batch = datetime.datetime.now()

    files = glob.glob(pattern)
    for i, filename in enumerate(files):
        try:

            before = datetime.datetime.now()
            pdb.gimp_message("{} Starting ({}/{}) {}...".format(before, i+1, len(files), filename))
            destination_file = os.path.join(destination_folder, os.path.basename(filename))

            image = pdb.gimp_file_load(filename, filename)
        
            remove_photosphere_creator(image, image.active_drawable, height, False)
            pdb.file_jpeg_save(image,image.active_drawable,destination_file,destination_file, 1,0,1,1,"",2,0, 0,0)
            after = datetime.datetime.now()
            pdb.gimp_message("... took {}".format(after - before))
            success+=1

        except Exception, e:
            errors.append("({}/{}) {}: {}".format(i+1, len(files), filename, e));

    after_batch = datetime.datetime.now()

    if errors:
        pdb.gimp_message("Errors while processing the batch")
        for e in errors: pdb.gimp_message(e)
    else:
        pdb.gimp_message("Completed without errors")

    pdb.gimp_message("{} Finished, errors: {}, success: {}, took: {}".format(after_batch, len(errors), success, (after_batch - before_batch)))

def remove_photosphere_creator(image, drawable, height, only_select):
    gimp.progress_init("Remove the creator of the photosphere " + drawable.name + "...")
    pdb.gimp_image_undo_group_start(image)

    pdb.gimp_image_select_polygon(image, CHANNEL_OP_REPLACE,8,[0, image.height-height, image.width, image.height-height, image.width, image.height,0, image.height])
    
    for i in range(0, image.width, STEP):
 #       pdb.gimp_fuzzy_select_full(image.active_drawable, i, image.height-height, 10, CHANNEL_OP_SUBTRACT, True, False, 0, 0, False, True, SELECT_CRITERION_V)
        pdb.gimp_fuzzy_select_full(image.active_drawable, i, image.height-height, 5, CHANNEL_OP_SUBTRACT, True, False, 0, 0, False, True, SELECT_CRITERION_S)
        pdb.gimp_fuzzy_select_full(image.active_drawable, i, image.height-height, 12, CHANNEL_OP_SUBTRACT, True, False, 0, 0, False, True, SELECT_CRITERION_COMPOSITE)
#        pdb.gimp_selection_shrink(image, 5)
 #       pdb.gimp_selection_grow(image, 5)
#        pdb.gimp_paintbrush_default(drawable, 2, [i, image.height-height])
#    for i in range(STEP/2, image.width, STEP):
#        pdb.gimp_fuzzy_select_full(image.active_drawable, i, image.height-height - STEP, 5, CHANNEL_OP_SUBTRACT, True, False, 0, 0, False, True, SELECT_CRITERION_V)
#        pdb.gimp_fuzzy_select_full(image.active_drawable, i, image.height-height - STEP, 10, CHANNEL_OP_SUBTRACT, True, False, 0, 0, False, True, SELECT_CRITERION_S)
#        pdb.gimp_fuzzy_select_full(image.active_drawable, i, image.height-height- STEP, 10, CHANNEL_OP_SUBTRACT, True, False, 0, 0, False, True, SELECT_CRITERION_COMPOSITE)
 #       pdb.gimp_paintbrush_default(drawable, 2, [i, image.height-height -STEP])
    pdb.gimp_selection_shrink(image, 10)
    pdb.gimp_selection_grow(image, 15)
    #pdb.gimp_selection_border( image,5)
    #pdb.gimp_edit_clear(drawable)
    if not only_select: pdb.python_fu_heal_selection(image, drawable, 50, 0, 0);

    pdb.gimp_image_undo_group_end(image)

register(
    "python_fu_remove_photosphere_creator",
    "Remove the creator of the photosphere",
    "Remove the creator of the photosphere",
    "Plamen Tanov",
    "Plamen Tanov",
    "2018",
    "Remove the creator of the photosphere",
    "*",
    [
        (PF_IMAGE, "image", "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None),
        (PF_INT, "height", "How much to select (e.g. 320)?", DEFAULT_HEIGHT),
        (PF_BOOL, "only_select", "Select only, without healing/removing", False)
    ],
    [],
    remove_photosphere_creator, menu="<Image>/Filters/Enhance")

register(
    "python_fu_remove_photosphere_creator_batch",
    "Remove the creator of the photosphere - batch",
    "Remove the creator of the photosphere - batch",
    "Plamen Tanov",
    "Plamen Tanov",
    "2018",
    "Remove the creator of the photosphere - batch",
    "*",
    [
        (PF_STRING, "string", "File pattern", None),
        (PF_STRING, "string", "Destination folder", None),
        (PF_INT, "height", "How much to select (e.g. 320)?", DEFAULT_HEIGHT)
    ],
    [],
    remove_photosphere_creator_batch)

main()

