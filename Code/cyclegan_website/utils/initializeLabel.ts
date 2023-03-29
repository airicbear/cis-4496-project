export const initializeLabel = function (
  label: HTMLElement,
  backgroundImage: string
) {
  label.style.backgroundImage = backgroundImage;
  label.style.backgroundSize = "100% 100%";
  label.style.backgroundRepeat = "no-repeat";
  label.textContent = "";
};
