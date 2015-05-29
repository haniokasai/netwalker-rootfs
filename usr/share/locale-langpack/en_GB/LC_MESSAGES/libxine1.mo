��    +      t  ;   �      �    �     9  �   X  o   *    �  �   �  �   �	  ?  #
  -  c    �  :  �  �   �  �   �  �   Z  �   0  �  �  �   l  �   J     4  W   G  �  �  .  �!  2  �"  
  �$  p  �%  �   b'     #(  b   A(     �(  8   �(     �(     �(  #   )     ?)     X)  9   w)  @   �)  >   �)  '   1*  .   Y*  �  �*  :   q.  �  �.    �0     3  �   93  o   4    {4  �   �5  �   t6  A  7  -  G8    u9  :  �?  �   �@  �   �A  �   ?B  �   C  �  �C  �   UH  �   3I     J  W   0J  �  �J  .  mN  8  �O  
  �Q  t  �R  �   UT     U  a   4U     �U  9   �U     �U     �U  #   V     2V     KV  9   jV  @   �V  >   �V  '   $W  .   LW  �  {W  ;   d[                                                           
                     %                    +   "                             $   '   (       #   	          )                   !      &   *           Alternative software equalizer that uses lookup tables (very slow), allowing gamma correction in addition to simple brightness, contrast and saturation adjustment.
Note that it uses the same MMX optimized code as 'eq' if all gamma values are 1.0.

Parameters
  gamma
  brightness
  contrast
  saturation
  rgamma (gamma for the red component)
  ggamma (gamma for the green component)
  bgamma (gamma for the blue component)

Value ranges are 0.1 - 10 for gammas, -2 - 2 for contrast (negative values result in a negative image), -1 - 1 for brightness and 0 - 3 for saturation.

* mplayer's eq2 (C) Hampa Hug, Daniel Moreno, Richard Felker
 DirectSound wasn't initialized Double buffering will synchronize the update of the video image to the repainting of the entire screen ("vertical retrace"). This eliminates flickering and tearing artifacts, but will use more graphics memory. Enable synchronizing the update of the video image to the repainting of the entire screen ("vertical retrace"). Enables CDDB queries, which will give you convenient title and track names for your audio CDs.
Keep in mind that, unless you use your own private CDDB, this information is retrieved from an internet server which might collect a profile of your listening habits. Enables a small logic that corrects the frame durations of some mpeg streams with wrong framerate codes. Currently a correction for NTSC streams erroneously labeled as PAL streams is implemented. Enable only, when you encounter such streams. For OpenGL double buffering does not only remove tearing artifacts,
it also reduces flickering a lot.
It should not have any performance impact. Mosaico does simple picture in picture effects.

Parameters
  pip_num: the number of the picture slot the following settings apply to
  x: the x coordinate of the left upper corner of the picture
  y: the y coordinate of the left upper corner of the picture
  w: the width of the picture
  h: the height of the picture
 Normalizes audio by maximizing the volume without distorting the sound.

Parameters:
  method: 1: use a single sample to smooth the variations via the standard weighted mean over past samples (default); 2: use several samples to smooth the variations via the standard weighted mean over past samples.
 Select how your speakers are arranged, this determines which speakers xine uses for sound output. The individual values are:

Mono 1.0: You have only one speaker.
Stereo 2.0: You have two speakers for left and right channel.
Headphones 2.0: You use headphones.
Stereo 2.1: You have two speakers for left and right channel, and one subwoofer for the low frequencies.
Surround 3.0: You have three speakers for left, right and rear channel.
Surround 4.0: You have four speakers for front left and right and rear left and right channels.
Surround 4.1: You have four speakers for front left and right and rear left and right channels, and one subwoofer for the low frequencies.
Surround 5.0: You have five speakers for front left, center and right and rear left and right channels.
Surround 5.1: You have five speakers for front left, center and right and rear left and right channels, and one subwoofer for the low frequencies.
Surround 6.0: You have six speakers for front left, center and right and rear left, center and right channels.
Surround 6.1: You have six speakers for front left, center and right and rear left, center and right channels, and one subwoofer for the low frequencies.
Surround 7.1: You have seven speakers for front left, center and right, left and right and rear left and right channels, and one subwoofer for the low frequencies.
Pass Through: Your sound system will receive undecoded digital sound from xine. You need to connect a digital surround decoder capable of decoding the formats you want to play to your sound card's digital output. Software equalizer with interactive controls just like the hardware equalizer, for cards/drivers that do not support brightness and contrast controls in hardware.

Parameters
  brightness
  contrast

Note: It is possible to use frontend's control window to set these parameters.

* mplayer's eq (C) Richard Felker
 Specifies the base part of the audio device name, to which the OSS device number is appended to get the full device name.
Select "auto" if you want xine to auto detect the corret setting. Specify the bandwidth of your internet connection here. This will be used when streaming servers offer different versions with different bandwidth requirements of the same stream. The copying of large memory blocks is one of the most expensive operations on todays computers. Therefore xine provides various tuned methods to do this copying. Usually, the best method is detected automatically. The encoding quality of the libfame mpeg encoder library. Lower is faster but gives noticeable artifacts. Higher is better but slower. This config setting is deprecated. You should use the new deinterlacing post processing settings instead.

From the old days of analog television, where the even and odd numbered lines of a video frame would be displayed at different times comes the idea to increase motion smoothness by also recording the lines at different times. This is called "interlacing". But unfortunately, todays displays show the even and odd numbered lines as one complete frame all at the same time (called "progressive display"), which results in ugly frame errors known as comb artifacts. Software deinterlacing is an approach to reduce these artifacts. The individual values are:

none
Disables software deinterlacing.

bob
Interpolates between the lines for moving parts of the image.

weave
Similar to bob, but with a tendency to preserve the full resolution, better for high detail in low movement scenes.

greedy
Very good adaptive deinterlacer, but needs a lot of CPU power.

onefield
Always interpolates and reduces vertical resolution.

onefieldxv
Same as onefield, but does the interpolation in hardware.

linearblend
Applies a slight vertical blur to remove the comb artifacts. Good results with medium CPU usage. This filter will perform a time stretch, playing the stream faster or slower by a factor. Pitch is optionally preserved, so it is possible, for example, to use it to watch a movie in less time than it was originaly shot.
 Tries to set a synchronization timestamp for every frame. Normally this is not necessary, because sync is sufficent even when the timestamp is set only every now and then.
This is relevant for progressive video only (most PAL films). Unichrome cpu save When enabled, closed captions will be positioned by the center of the individual lines. When playing audio and video, there are at least two clocks involved: The system clock, to which video frames are synchronized and the clock in your sound hardware, which determines the speed of the audio playback. These clocks are never ticking at the same speed except for some rare cases where they are physically identical. In general, the two clocks will run drift after some time, for which xine offers two ways to keep audio and video synchronized:

metronom feedback
This is the standard method, which applies a countereffecting video drift, as soon as the audio drift has accumulated over a threshold.

resample
For some video hardware, which is limited to a fixed frame rate (like the DXR3 or other decoder cards) the above does not work, because the video cannot drift. Therefore we resample the audio stream to make it longer or shorter to compensate the audio drift error. This does not work for digital passthrough, where audio data is passed to an external decoder in digital form. You can adjust the amount of post processing applied to MPEG-4 video.
Higher values result in better quality, but need more CPU. Lower values may result in image defects like block artifacts. For high quality content, too heavy post processing can actually make the image worse by blurring it too much. You can configure the behaviour when issuing a skip command (using the skip buttons for example). The individual values mean:

skip program
will skip a DVD program, which is a navigational unit similar to the index marks on an audio CD; this is the normal behaviour for DVD players

skip part
will skip a DVD part, which is a structural unit similar to the track marks on an audio CD; parts usually coincide with programs, but parts can be larger than programs

skip title
will skip a DVD title, which is a structural unit representing entire features on the DVD You can configure the behaviour when playing a dvd from a given title/chapter (eg. using MRL 'dvd:/1.2'). The individual values mean:

entire dvd
play the entire dvd starting on the specified position.

one chapter
play just the specified title/chapter and then stop You can configure the domain spanned by the seek slider. The individual values mean:

seek in program chain
seeking will span an entire DVD program chain, which is a navigational unit representing the entire video stream of the current feature

seek in program
seeking will span a DVD program, which is a navigational unit representing a chapter of the current feature audio_oss_out: Audio driver realtime sync disabled...
audio_oss_out: ...will use system real-time clock for soft-sync instead
audio_oss_out: ...there may be audio/video synchronization issues
 center-adjust closed captions input_rip: target directory wasn't specified, please fill out the option 'media.capture.save_dir'
 invalid url
 libareal: decoder flavor setup failed, error code: 0x%x
 maximum quantizer object was already initialized osd: cannot initialize ft2 library
 unrecognized FILM chunk
 use DVB 'center cutout' (zoom) video_out_fb: Your video mode was not recognized, sorry.
 video_out_xcbshm: your video mode was not recognized, sorry :-(
 video_out_xshm: your video mode was not recognized, sorry :-(
 w32codec: Error initializing DMO Audio
 w32codec: Error initializing DirectShow Audio
 xine can use different methods to keep audio and video synchronized. Which setting works best depends on the OSS driver and sound hardware you are using. Try the various methods, if you experience sync problems.

The meaning of the values is as follows:

auto
xine attempts to automatically detect the optimal setting

getodelay
uses the SNDCTL_DSP_GETODELAY ioctl to achieve true a/v sync even if the driver claims not to support realtime playback

getoptr
uses the SNDCTL_DSP_GETOPTR ioctl to achieve true a/v sync even if the driver supports the preferred SNDCTL_DSP_GETODELAY ioctl

softsync
uses software synchronization with the system clock; audio and video can get severely out of sync if the system clock speed does not precisely match your sound card's playback speed

probebuffer
probes the sound card buffer size on initialization to calculate the latency for a/v sync; try this if your system does not support any of the realtime ioctls and you experience sync errors after long playback xine video output plugin using the Color AsCii Art library Project-Id-Version: xine-lib
Report-Msgid-Bugs-To: FULL NAME <EMAIL@ADDRESS>
POT-Creation-Date: 2009-04-02 19:46+0100
PO-Revision-Date: 2007-11-20 16:18+0000
Last-Translator: Jen Ockwell <jenfraggleubuntu@googlemail.com>
Language-Team: English (United Kingdom) <en_GB@li.org>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=2; plural=n != 1;
X-Launchpad-Export-Date: 2009-04-14 10:09+0000
X-Generator: Launchpad (build Unknown)
 Alternative software equaliser that uses lookup tables (very slow), allowing gamma correction in addition to simple brightness, contrast and saturation adjustment.
Note that it uses the same MMX optimised code as 'eq' if all gamma values are 1.0.

Parameters
  gamma
  brightness
  contrast
  saturation
  rgamma (gamma for the red component)
  ggamma (gamma for the green component)
  bgamma (gamma for the blue component)

Value ranges are 0.1 - 10 for gammas, -2 - 2 for contrast (negative values result in a negative image), -1 - 1 for brightness and 0 - 3 for saturation.

* mplayer's eq2 (C) Hampa Hug, Daniel Moreno, Richard Felker
 DirectSound wasn't initialised Double buffering will synchronise the update of the video image to the repainting of the entire screen ("vertical retrace"). This eliminates flickering and tearing artefacts, but will use more graphics memory. Enable synchronising the update of the video image to the repainting of the entire screen ("vertical retrace"). Enables CDDB queries, which will give you convenient title and track names for your audio CDs.
Keep in mind that, unless you use your own private CDDB, this information is retrieved from an Internet server which might collect a profile of your listening habits. Enables a small logic that corrects the frame durations of some mpeg streams with wrong framerate codes. Currently a correction for NTSC streams erroneously labelled as PAL streams is implemented. Enable only, when you encounter such streams. For OpenGL double buffering does not only remove tearing artefacts,
it also reduces flickering a lot.
It should not have any performance impact. Mosaico does simple picture in picture effects.

Parameters
  pip_num: the number of the picture slot the following settings apply to
  x: the x co-ordinate of the left upper corner of the picture
  y: the y co-ordinate of the left upper corner of the picture
  w: the width of the picture
  h: the height of the picture
 Normalises audio by maximising the volume without distorting the sound.

Parameters:
  method: 1: use a single sample to smooth the variations via the standard weighted mean over past samples (default); 2: use several samples to smooth the variations via the standard weighted mean over past samples.
 Select how your speakers are arranged, this determines which speakers xine uses for sound output. The individual values are:

Mono 1.0: You have only one speaker.
Stereo 2.0: You have two speakers for left and right channel.
Headphones 2.0: You use headphones.
Stereo 2.1: You have two speakers for left and right channel, and one subwoofer for the low frequencies.
Surround 3.0: You have three speakers for left, right and rear channel.
Surround 4.0: You have four speakers for front left and right and rear left and right channels.
Surround 4.1: You have four speakers for front left and right and rear left and right channels, and one subwoofer for the low frequencies.
Surround 5.0: You have five speakers for front left, centre and right and rear left and right channels.
Surround 5.1: You have five speakers for front left, centre and right and rear left and right channels, and one subwoofer for the low frequencies.
Surround 6.0: You have six speakers for front left, centre and right and rear left, centre and right channels.
Surround 6.1: You have six speakers for front left, centre and right and rear left, centre and right channels, and one subwoofer for the low frequencies.
Surround 7.1: You have seven speakers for front left, centre and right, left and right and rear left and right channels, and one subwoofer for the low frequencies.
Pass Through: Your sound system will receive undecoded digital sound from xine. You need to connect a digital surround decoder capable of decoding the formats you want to play to your sound card's digital output. Software equaliser with interactive controls just like the hardware equaliser, for cards/drivers that do not support brightness and contrast controls in hardware.

Parameters
  brightness
  contrast

Note: It is possible to use frontend's control window to set these parameters.

* mplayer's eq (C) Richard Felker
 Specifies the base part of the audio device name, to which the OSS device number is appended to get the full device name.
Select "auto" if you want xine to auto detect the correct setting. Specify the bandwidth of your Internet connection here. This will be used when streaming servers offer different versions with different bandwidth requirements of the same stream. The copying of large memory blocks is one of the most expensive operations on today's computers. Therefore xine provides various tuned methods to do this copying. Usually, the best method is detected automatically. The encoding quality of the libfame mpeg encoder library. Lower is faster but gives noticeable artefacts. Higher is better but slower. This config setting is deprecated. You should use the new deinterlacing post processing settings instead.

From the old days of analogue television, where the even and odd numbered lines of a video frame would be displayed at different times comes the idea to increase motion smoothness by also recording the lines at different times. This is called "interlacing". But unfortunately, today's displays show the even and odd numbered lines as one complete frame all at the same time (called "progressive display"), which results in ugly frame errors known as comb artefacts. Software deinterlacing is an approach to reduce these artefacts. The individual values are:

none
Disables software deinterlacing.

bob
Interpolates between the lines for moving parts of the image.

weave
Similar to bob, but with a tendency to preserve the full resolution, better for high detail in low movement scenes.

greedy
Very good adaptive deinterlacer, but needs a lot of CPU power.

onefield
Always interpolates and reduces vertical resolution.

onefieldxv
Same as onefield, but does the interpolation in hardware.

linearblend
Applies a slight vertical blur to remove the comb artefacts. Good results with medium CPU usage. This filter will perform a time stretch, playing the stream faster or slower by a factor. Pitch is optionally preserved, so it is possible, for example, to use it to watch a film in less time than it was originally shot.
 Tries to set a synchronisation timestamp for every frame. Normally this is not necessary, because sync is sufficent even when the timestamp is set only every now and then.
This is relevant for progressive video only (most PAL films). Unichrome CPU save When enabled, closed captions will be positioned by the centre of the individual lines. When playing audio and video, there are at least two clocks involved: The system clock, to which video frames are synchronised and the clock in your sound hardware, which determines the speed of the audio playback. These clocks are never ticking at the same speed except for some rare cases where they are physically identical. In general, the two clocks will run drift after some time, for which xine offers two ways to keep audio and video synchronized:

metronom feedback
This is the standard method, which applies a countereffecting video drift, as soon as the audio drift has accumulated over a threshold.

resample
For some video hardware, which is limited to a fixed frame rate (like the DXR3 or other decoder cards) the above does not work, because the video cannot drift. Therefore we resample the audio stream to make it longer or shorter to compensate the audio drift error. This does not work for digital passthrough, where audio data is passed to an external decoder in digital form. You can adjust the amount of post processing applied to MPEG-4 video.
Higher values result in better quality, but need more CPU. Lower values may result in image defects like block artefacts. For high quality content, too heavy post processing can actually make the image worse by blurring it too much. You can configure the behaviour when issuing a skip command (using the skip buttons for example). The individual values mean:

skip program
will skip a DVD programme, which is a navigational unit similar to the index marks on an audio CD; this is the normal behaviour for DVD players

skip part
will skip a DVD part, which is a structural unit similar to the track marks on an audio CD; parts usually coincide with programmes, but parts can be larger than programmes

skip title
will skip a DVD title, which is a structural unit representing entire features on the DVD You can configure the behaviour when playing a DVD from a given title/chapter (eg. using MRL 'dvd:/1.2'). The individual values mean:

entire dvd
play the entire DVD starting on the specified position.

one chapter
play just the specified title/chapter and then stop You can configure the domain spanned by the seek slider. The individual values mean:

seek in program chain
seeking will span an entire DVD programme chain, which is a navigational unit representing the entire video stream of the current feature

seek in program
seeking will span a DVD programme, which is a navigational unit representing a chapter of the current feature audio_oss_out: Audio driver realtime sync disabled...
audio_oss_out: ...will use system real-time clock for soft-sync instead
audio_oss_out: ...there may be audio/video synchronisation issues
 centre-adjust closed captions input_rip: target directory wasn't specified, please fill in the option 'media.capture.save_dir'
 invalid URL
 libareal: decoder flavour setup failed, error code: 0x%x
 maximum quantiser object was already initialised osd: cannot initialise ft2 library
 unrecognised FILM chunk
 use DVB 'centre cutout' (zoom) video_out_fb: Your video mode was not recognised, sorry.
 video_out_xcbshm: your video mode was not recognised, sorry :-(
 video_out_xshm: your video mode was not recognised, sorry :-(
 w32codec: Error initialising DMO Audio
 w32codec: Error initialising DirectShow Audio
 xine can use different methods to keep audio and video synchronised. Which setting works best depends on the OSS driver and sound hardware you are using. Try the various methods, if you experience sync problems.

The meaning of the values is as follows:

auto
xine attempts to automatically detect the optimal setting

getodelay
uses the SNDCTL_DSP_GETODELAY ioctl to achieve true a/v sync even if the driver claims not to support realtime playback

getoptr
uses the SNDCTL_DSP_GETOPTR ioctl to achieve true a/v sync even if the driver supports the preferred SNDCTL_DSP_GETODELAY ioctl

softsync
uses software synchronisation with the system clock; audio and video can get severely out of sync if the system clock speed does not precisely match your sound card's playback speed

probebuffer
probes the sound card buffer size on initialisation to calculate the latency for a/v sync; try this if your system does not support any of the realtime ioctls and you experience sync errors after long playback xine video output plugin using the Colour AsCii Art library 