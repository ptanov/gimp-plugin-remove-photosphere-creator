# gimp-plugin-remove-photosphere-creator

This plugin tries to remove the creator of photospheres (360&deg; photos) in [equirectangular projection](https://www.google.com/search?q=360+equirectangular+projection&tbm=isch). Usually the creator is placed in the bottom of the image (when it is in [equirectangular projection](https://www.google.com/search?q=360+equirectangular+projection&tbm=isch)). It is not very precise but it works relatively good to remove at least your identity - [good example for removing the creator](https://www.google.bg/maps/@42.5900993,23.2934551,3a,90y,359.37h,39.63t/data=!3m8!1e1!3m6!1sAF1QipOk_nyXzM126xfCaYtYH1ToaI3e0tNx0cTfUY5K!2e10!3e12!6shttps:%2F%2Flh5.googleusercontent.com%2Fp%2FAF1QipOk_nyXzM126xfCaYtYH1ToaI3e0tNx0cTfUY5K%3Dw520-h260-k-no!7i5760!8i2880), and [not so good example](https://www.google.bg/maps/contrib/115955919389881836828/photos/@42.5906792,23.2931156,3a,89.8y,9.91h,42.28t/data=!3m7!1e1!3m5!1sAF1QipPl16QzfV9V3gIWsC_Tw6JOu7QKtVTKJjQXfhYF!2e10!6shttps:%2F%2Flh5.googleusercontent.com%2Fp%2FAF1QipPl16QzfV9V3gIWsC_Tw6JOu7QKtVTKJjQXfhYF%3Dw520-h260-k-no!7i5760!8i2880!4m3!8m2!3m1!1e1).


# Running

There are two options for running the script - automatic (for batch processing) and manual. Both options can be runned using local gimp installation or using docker.

## Automatic

### local GIMP installation

 - Install GIMP. In Ubuntu just run `sudo apt install gimp`
 - Install [GIMP Resynthesizer Plugin](https://templatetoaster.com/tutorials/gimp-resynthesizer-plugin/). In Ubuntu just run `sudo apt install gimp-plugins-registry`. For more information for your specific system: <https://templatetoaster.com/tutorials/gimp-resynthesizer-plugin/>

You should copy the [remove photosphere creator plugin](https://raw.githubusercontent.com/ptanov/gimp-plugin-remove-photosphere-creator/master/remove_photosphere_creator.py) into GIMP plugin folder. In Ubuntu it is located `~/.gimp-2.8/plug-ins` for the current user and `/usr/lib/gimp/2.0/plug-ins/` for all users. Make sure that the script is executable (e.g. `chmod +x ~/.gimp-2.8/plug-ins/remove_photosphere_creator.py`. For detailed instructions on how to install GIMP plugin you can reference <https://templatetoaster.com/tutorials/gimp-resynthesizer-plugin/>.

Then simply run the command and wait for it (it will took some time): `gimp -i -b '(python-fu-remove-photosphere-creator-batch 0 "*.JPG" "/home/USER/DESTINATIONFOLDER" 580 )' -b '(gimp-quit 0)'`, where:
 - `*.JPG` - files to process (in current folder). They must be 360 photos (photospheres) in [equirectangular projection](https://www.google.com/search?q=360+equirectangular+projection&tbm=isch).
 - `/home/USER/DESTINATIONFOLDER` - where to put the the result (healed files)
 - `580` - pixels from the bottom that need to be inspected for the photosphere creator. See [Algorithm explanation](#Algorithm) for more information.

### using docker

 - `docker run --rm -it -e DISPLAY -v ~/.Xauthority:/root/.Xauthority -v /tmp/.X11-unix/:/tmp/.X11-unix/ -v /dev/dri/:/dev/dri/ --device=/dev/snd -v $(pwd):$(pwd) -v $(pwd):/data --name=gimp-plugin-remove-photosphere-creator ptanov/gimp-plugin-remove-photosphere-creator gimp -i -b '(python-fu-remove-photosphere-creator-batch 0 "*.JPG" "processed/" 580 )' -b '(gimp-quit 0)'`, where
   - `*.JPG` - files to process (in current folder). They must be 360 photos (photospheres) in [equirectangular projection](https://www.google.com/search?q=360+equirectangular+projection&tbm=isch).
   - `processed/` - where to put the the result (healed files)
   - `580` - pixels from the bottom that need to be inspected for the photosphere creator. See [Algorithm explanation](#Algorithm) for more information.

## Manual

### local GIMP installation

 - Install GIMP. In Ubuntu just run `sudo apt install gimp`
 - Install [GIMP Resynthesizer Plugin](https://templatetoaster.com/tutorials/gimp-resynthesizer-plugin/). In Ubuntu just run `sudo apt install gimp-plugins-registry`. For more information for your specific system: <https://templatetoaster.com/tutorials/gimp-resynthesizer-plugin/>

You should copy the [remove photosphere creator plugin](https://raw.githubusercontent.com/ptanov/gimp-plugin-remove-photosphere-creator/master/remove_photosphere_creator.py) into GIMP plugin folder. In Ubuntu it is located `~/.gimp-2.8/plug-ins` for the current user and `/usr/lib/gimp/2.0/plug-ins/` for all users. Make sure that the script is executable (e.g. `chmod +x ~/.gimp-2.8/plug-ins/remove_photosphere_creator.py`. For detailed instructions on how to install GIMP plugin you can reference <https://templatetoaster.com/tutorials/gimp-resynthesizer-plugin/>.

 - Start GIMP
   - Open image that is photosphere (360&deg; photo) in [equirectangular projection](https://www.google.com/search?q=360+equirectangular+projection&tbm=isch)
   - Use `Filters > Enhance > Remove the creator of the photosphere`, where:
     - `How much to select (e.g. 320)?` pixels from the bottom that need to be inspected for the photosphere creator. See [Algorithm explanation](#Algorithm) for more information
     - `Select only, without healing/removing` - if you want to fix the selection before running `Filters > Enhance > Heal Selection...` 

### using docker

 - `docker run --rm -it -e DISPLAY -v ~/.Xauthority:/root/.Xauthority -v /tmp/.X11-unix/:/tmp/.X11-unix/ -v /dev/dri/:/dev/dri/ --device=/dev/snd -v $(pwd):$(pwd) -v $(pwd):/data --name=gimp-plugin-remove-photosphere-creator ptanov/gimp-plugin-remove-photosphere-creator`
 - Open image that is photosphere (360&deg; photo) in [equirectangular projection](https://www.google.com/search?q=360+equirectangular+projection&tbm=isch)
 - Use `Filters > Enhance > Remove the creator of the photosphere`, where:
   - `How much to select (e.g. 320)?` pixels from the bottom that need to be inspected for the photosphere creator. See [Algorithm explanation](#Algorithm) for more information
   - `Select only, without healing/removing` - if you want to fix the selection before running `Filters > Enhance > Heal Selection...` 

# Algorithm

The algorithm is really simple - the scripts selects the bottom of the image (user defined pixels count) and then uses fuzzy select on multiple points above the line to unselect the region that is similar to the upper part of the image. You can see it in action step by step in [Manual mode](#Manual).


