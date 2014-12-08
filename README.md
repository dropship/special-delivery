special-delivery
================

#### Dropship Pd Generative Music Engine
This is a complete generative music system that creates constantly evolving modern Dubstep music, using a range of algorithmic composition techniques.
##### Running the patch
The patch runs in [Pd-vanilla](http://puredata.info/downloads/pure-data), and any required externals are included. The externals (u_storechord, seq, midiparse etc.) have only been tested for Mac OS.  
1. Install [Pd-vanilla](http://puredata.info/downloads/pure-data) and clone this repo
2. Download the supporting audio files
from [here](https://www.dropbox.com/s/wx8oejh02npwjer/audio.zip?dl=0) and move the ```audio``` folder into the root directory
3.  Open ```_main.pd``` in the root directory

##### Audio samples
These are SoundCloud clips of this patch either just running in ambient mode, or looping the drop section lots of times.  
[Ambient section](https://soundcloud.com/mohosounds/dropship-ambient-sample-3)  
[Drops](https://soundcloud.com/mohosounds/dropship-drops)
##### How to use this patch
As with many things in algorithmic composition, implementations of a particular idea or way of doing something are very specific to their use-case. Therefore look at this patch more as a practical reference point for various techniques of generating melodies, harmonies and rhythms for popular music genres.  
Pause the auto-play of the arrangement in ```[pd ambient-structure]```, which makes it easier to inspect individual instruments without the track progressing automatically.
##### Other resources
There are comments all over the patch where I feel the objects need further explaining, but there are also some longer-form blog-posts covering various methods and techniques here:
- [Composing Drops To Ship](http://dropship.github.io/update/2014/05/05/composing-drops-to-ship.html)
- [Diving into the sPiDers web](http://dropship.github.io/update/2014/05/12/diving-into-the-spiders-web.html)
- [Drop timings and endless techno](http://dropship.github.io/update/2014/05/21/drop-timings-and-endless-techno.html)
- [Music Update - Ambient](http://dropship.github.io/update/2014/07/20/music-update.html)