export const Colors = {
  light: {
    text: '#000',
    background: '#fff',
    tint: '#0A84FF',
    icon: '#222',
  },
  dark: {
    text: '#fff',
    background: '#000',
    tint: '#0A84FF',
    icon: '#fff',
  },
} as const;

export type ColorScheme = keyof typeof Colors;
