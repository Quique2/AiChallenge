import { useMutation } from '@tanstack/react-query';
import { router, useLocalSearchParams } from 'expo-router';
import { Alert, ScrollView, StyleSheet, View } from 'react-native';

import { Button } from '@/components/button';
import { Group, GroupRow } from '@/components/group';
import { Notice } from '@/components/notice';
import { QueryFeedback } from '@/components/query-feedback';
import { ThemedText } from '@/components/themed-text';
import { MaxContentWidth, Spacing } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';
import { useLocale, useT } from '@/i18n';
import { api } from '@/lib/api';
import { keys, queryClient, useLabels, useMemory } from '@/lib/queries';

/**
 * "Lo que sé de este lugar": lo que suele molestar aquí, lo que se probó (ayudara o no, con sus
 * números reales) y lo que no se puede hacer. Es la vista simple del cuarto: la misma información
 * sin dibujo. "Usarlo otra vez" abre un registro corto que va directo a ese ajuste.
 */
export default function Place() {
  const t = useT();
  const theme = useTheme();
  const locale = useLocale();
  const labels = useLabels();
  const { id } = useLocalSearchParams<{ id: string }>();
  const memory = useMemory(id);
  const data = memory.data;
  const blocked = new Set((data?.blocked ?? []).map((a) => a.id));

  const reset = useMutation({
    mutationFn: () => api.resetSpace(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: keys.memory(id) });
      queryClient.invalidateQueries({ queryKey: keys.playbook });
    },
  });

  function confirmReset() {
    Alert.alert(t.place.changedConfirmTitle, t.place.changedConfirmBody, [
      { text: t.settings.cancel, style: 'cancel' },
      { text: t.place.changedConfirm, onPress: () => reset.mutate() },
    ]);
  }

  function repeatAdjustment(adjustment: string, stimulus: string | null) {
    router.push({ pathname: '/checkin/repeat', params: { adjustment, stimulus: stimulus ?? '', space: id } });
  }

  return (
    <ScrollView
      contentInsetAdjustmentBehavior="automatic"
      style={{ backgroundColor: theme.background }}
      contentContainerStyle={styles.content}>
      <QueryFeedback query={memory} />

      {data ? (
        <>
          <View style={styles.heading}>
            <ThemedText type="title" accessibilityRole="header">
              {data.space.name}
            </ThemedText>
            <ThemedText type="callout" themeColor="textSecondary">
              {data.trials ? t.place.counter(data.trials, data.known) : t.place.empty}
            </ThemedText>
          </View>

          {data.stimuli.length ? (
            <Group title={t.place.stimuliTitle}>
              {data.stimuli.map((item, index) => (
                <GroupRow key={item.stimulus} first={index === 0}>
                  <View style={styles.row}>
                    <ThemedText style={styles.flex}>{item.label}</ThemedText>
                    <ThemedText type="footnote" themeColor="textSecondary">
                      {t.place.times(item.times)}
                    </ThemedText>
                  </View>
                </GroupRow>
              ))}
            </Group>
          ) : null}

          {data.tried.length ? (
            <Group title={t.place.triedTitle} footer={t.place.triedFooter}>
              {data.tried.map((entry, index) => (
                <GroupRow key={entry.adjustment.id} first={index === 0}>
                  <ThemedText type="bodyStrong">{entry.adjustment.title}</ThemedText>
                  <ThemedText type="footnote" themeColor="textSecondary">
                    {[
                      entry.stimulus ? t.playbook.forStimulus(labels.stimulus(entry.stimulus)) : null,
                      t.place.evidence(entry.helped, entry.trials),
                    ]
                      .filter(Boolean)
                      .join(' · ')}
                  </ThemedText>
                  {blocked.has(entry.adjustment.id) ? null : (
                    <Button
                      variant="secondary"
                      title={t.place.useAgain}
                      accessibilityHint={entry.adjustment.title}
                      onPress={() => repeatAdjustment(entry.adjustment.id, entry.stimulus)}
                    />
                  )}
                </GroupRow>
              ))}
            </Group>
          ) : null}

          {data.blocked.length ? (
            <Group title={t.place.blockedTitle}>
              {data.blocked.map((adjustment, index) => (
                <GroupRow key={adjustment.id} first={index === 0}>
                  <ThemedText>{adjustment.title}</ThemedText>
                </GroupRow>
              ))}
            </Group>
          ) : null}

          <Group title={t.place.changedTitle}>
            <GroupRow first>
              <ThemedText type="callout">{t.place.changedBody}</ThemedText>
              {data.space.reset_at ? (
                <ThemedText type="footnote" themeColor="textSecondary">
                  {t.place.changedOn(new Date(data.space.reset_at).toLocaleDateString(locale))}
                </ThemedText>
              ) : null}
              <Button
                variant="plain"
                title={t.place.changed}
                loading={reset.isPending}
                style={styles.inline}
                onPress={confirmReset}
              />
            </GroupRow>
          </Group>
          {reset.isError ? <Notice text={t.common.somethingFailed} /> : null}
        </>
      ) : null}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  content: {
    padding: Spacing.three,
    paddingBottom: Spacing.six,
    gap: Spacing.four,
    width: '100%',
    maxWidth: MaxContentWidth,
    alignSelf: 'center',
  },
  heading: {
    gap: Spacing.two,
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.three,
  },
  flex: {
    flex: 1,
  },
  inline: {
    alignSelf: 'flex-start',
    paddingHorizontal: 0,
    minHeight: 44,
  },
});
