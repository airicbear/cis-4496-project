export const getRGB = (img: HTMLImageElement) => {
  const rD = {};
  const gD = {};
  const bD = {};

  const cv = document.createElement("canvas");
  const ctx = cv.getContext("2d");
  cv.width = img.width;
  cv.height = img.height;
  ctx.drawImage(img, 0, 0);
  const iD = ctx.getImageData(0, 0, cv.width, cv.height).data;

  for (let i = 0; i < 256; i++) {
    rD[i] = 0;
    gD[i] = 0;
    bD[i] = 0;
  }

  for (let i = 0; i < iD.length; i += 4) {
    rD[iD[i]]++;
    gD[iD[i + 1]]++;
    bD[iD[i + 2]]++;
  }

  return { rD, gD, bD };
};
