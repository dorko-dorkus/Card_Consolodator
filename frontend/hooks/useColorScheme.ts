import { ColorSchemeName, useColorScheme as useRNScheme } from 'react-native';

// A hook that returns the device color scheme. If unavailable, returns null.
export function useColorScheme(): ColorSchemeName {
  return useRNScheme();
}
