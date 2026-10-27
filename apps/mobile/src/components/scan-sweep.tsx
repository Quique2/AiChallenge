import { useEffect, useState } from 'react';
import { StyleSheet, View } from 'react-native';
import Animated, {
  cancelAnimation,
  Easing,
  useAnimatedStyle,
  useSharedValue,
  withRepeat,
  withTiming,
} from 'react-native-reanimated';

import { useTheme } from '@/hooks/use-theme';
import { useMotionLevel } from '@/lib/feedback';

const BAND = 0.16;

/**
 * Mientras se analiza la foto, una franja la recorre de arriba abajo y de vuelta: se ve que algo
 * está pasando sin girar un spinner encima de la imagen. Con detalles, el borde de la franja es
 * una fila de pixeles. Con movimiento reducido no se muestra (el texto ya dice "Analizando…").
 */
export function ScanSweep({ active }: { active: boolean }) {
  const theme = useTheme();
  const level = useMotionLevel();
  const [height, setHeight] = useState(0);
  const position = useSharedValue(0);
  const running = active && level !== 'reduced' && height > 0;

  useEffect(() => {
    if (!running) {
      cancelAnimation(position);
      return;
    }
    position.value = withRepeat(withTiming(1, { duration: 1600, easing: Easing.linear }), -1, true);
    return () => cancelAnimation(position);
  }, [running, position]);

  const band = height * BAND;
  const style = useAnimatedStyle(() => ({ transform: [{ translateY: position.value * (height - band) }] }));

  return (
    <View
      style={StyleSheet.absoluteFill}
      pointerEvents="none"
      onLayout={(event) => setHeight(event.nativeEvent.layout.height)}>
      {running ? (
        <Animated.View style={[styles.band, { height: band }, style]}>
          <View style={[StyleSheet.absoluteFill, { backgroundColor: theme.primary, opacity: 0.16 }]} />
          {level === 'detailed' ? (
            <View style={styles.pixels}>
              {Array.from({ length: 24 }, (_, index) => (
                <View
                  key={index}
                  style={[styles.pixel, { backgroundColor: theme.onPrimary, opacity: index % 2 ? 0.9 : 0.5 }]}
                />
              ))}
            </View>
          ) : (
            <View style={[styles.line, { backgroundColor: theme.onPrimary }]} />
          )}
        </Animated.View>
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  band: {
    position: 'absolute',
    left: 0,
    right: 0,
    justifyContent: 'flex-end',
  },
  line: {
    height: 3,
    opacity: 0.85,
  },
  pixels: {
    flexDirection: 'row',
    height: 6,
  },
  pixel: {
    flex: 1,
  },
});
