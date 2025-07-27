export const Colors = {
  light: {
    text: '#1A1A1A',
    background: '#F5F6FA',
    tint: '#6D4AFF',
    icon: '#6D4AFF',
  },
  dark: {
    text: '#E5E5E5',
    background: '#121212',
    tint: '#A491FF',
    icon: '#A491FF',
  },
} as const;

export type ColorScheme = keyof typeof Colors;
