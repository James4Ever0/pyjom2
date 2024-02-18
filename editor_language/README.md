language specification for video editing

```
PICK clip_id
INFO clip_id
ANALYZE clip_id
CREATE clip_start clip_end clip_id
CROP x0 y0 x1 y1 clip_start clip_end clip_id
CROP_ROT x0 y0 x1 y1 rot clip_start clip_end clip_id
CUT clip_start clip_end clip_id
CHECK_CLIPS
SEARCH clip_info
SPLIT clip_id
SPLIT_AUDIO audio_clip_id
INSERT timestamp clip_id track_id
NEW_TRACK
VIEW_TRACK
VIEW_PROJECT
ZOOM_IN
ZOOM_OUT
FORWARD_POSITION
BACKWARD_POSITION
FORWARD_TRACK
BACKWARD_TRACK
MARK timestamp comment
APPLY effect_id effect_parameters clip_id
SUBMIT
```

---

better hands on video editing and enrich this video editing language syntax

---

the training perspective: time reverse training method.

if what is being applied to the existing video clip is messy, try to do it in reverse, so that it will be restored into a good clip ready for release.

you can mask certain clips, mangle the image, text, voice and ask the model to fill in.

you can also apply a scoring perspective, using video critic trained on viewer statistics.