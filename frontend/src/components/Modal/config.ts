export const modalSizeVariants = {
  small: `
    w-11/12 max-w-sm   h-auto max-h-[80vh]   /* almost full width on mobile */
    sm:w-3/4 sm:max-w-md
    md:w-1/2 md:max-w-lg
  `,
  default: `
    w-11/12 max-w-md h-auto max-h-[85vh]
    sm:w-3/4 sm:max-w-lg
    md:w-2/3 md:max-w-2xl
    lg:w-1/2 lg:max-w-3xl
    min-h-1/2
  `,
  large: `
    w-11/12 h-8/10
    sm:w-4/5 sm:max-w-3xl
    md:w-3/4 md:max-w-4xl
    lg:w-2/3 lg:max-w-5xl
  `,
};

export type ModalSizeVariants = keyof typeof modalSizeVariants;
