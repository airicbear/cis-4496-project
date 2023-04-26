export function imageToDataUri(
  img: HTMLImageElement,
  width: number,
  height: number
) {
  let canvas = document.createElement("canvas");
  let ctx = canvas.getContext("2d");

  canvas.width = width;
  canvas.height = height;

  ctx?.drawImage(img, 0, 0, width, height);

  return canvas.toDataURL("image/jpeg", 1.0);
}
