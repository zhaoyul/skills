# Image policy

## EPUB

Extract original image binaries whenever possible. Keep source href -> output path -> SHA-256 mapping.

## PDF

Preferred order:

1. direct embedded image extraction when the embedded object is the complete figure;
2. otherwise render at 288 DPI and crop the figure bounds;
3. if a figure is split by text/caption, crop the components and reconstruct on a white canvas following the original layout.

Exclude unrelated header/footer/page number/body text. If the caption is represented as translated Org text, do not duplicate it inside the crop.

Whole-page screenshots are only acceptable when the page itself is an inseparable visual object and the exception is documented.
