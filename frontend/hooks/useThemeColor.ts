import { Colors, ColorScheme } from '@/constants/Colors';
import { useColorScheme } from './useColorScheme';

type ThemeProps = {
  light?: string;
  dark?: string;
};

export function useThemeColor(
  props: ThemeProps,
  colorName: keyof typeof Colors.light
) {
  const theme: ColorScheme = useColorScheme() ?? 'light';
  const colorFromProps = props[theme];
  if (colorFromProps) {
    return colorFromProps;
  }
  return Colors[theme][colorName];
}
