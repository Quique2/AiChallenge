import { router } from 'expo-router';
import { RefreshControl, ScrollView, StyleSheet, View } from 'react-native';

import { Button } from '@/components/button';
import { DeskScene } from '@/components/desk/desk-scene';
import { Group, GroupRow } from '@/components/group';
import { Notice } from '@/components/notice';
import { ThemedText } from '@/components/themed-text';
import { MaxContentWidth, Spacing } from '@/constants/theme';
import { useTheme } from '@/hooks/use-theme';
import { useT } from '@/i18n';
import { deskItems } from '@/lib/desk';
import { useMotionLevel } from '@/lib/feedback';
import { useLabels, usePlaybook, useTrying } from '@/lib/queries';
import { useSettings } from '@/lib/settings';

export default function Today() {
  const t = useT();
  const theme = useTheme();
  const labels = useLabels();
  const level = useMotionLevel();
  const { settings, update } = useSettings();
  const trying = useTrying();
  const playbook = usePlaybook();
  const lastHelped = playbook.data?.[0];
  const items = deskItems(playbook.data);

  function refresh() {
    trying.refetch();
    playbook.refetch();
  }

  return (
    <ScrollView
      contentInsetAdjustmentBehavior="automatic"
      style={{ backgroundColor: theme.background }}
      contentContainerStyle={styles.content}
      refreshControl={<RefreshControl refreshing={trying.isRefetching} onRefresh={refresh} />}>
      {trying.data?.length ? (
        <Group title={t.today.tryingTitle}>
          {trying.data.map((checkin, index) => (
            <GroupRow key={checkin.id} first={index === 0}>
              <ThemedText type="bodyStrong">{checkin.adjustment?.title}</ThemedText>
              <ThemedText type="footnote" themeColor="textSecondary">
                {[labels.task(checkin.task), checkin.space?.name].filter(Boolean).join(' · ')}
              </ThemedText>
              <Button
                variant="secondary"
                title={t.today.tellMe}
                onPress={() => router.push({ pathname: '/checkout/[id]', params: { id: checkin.id } })}
              />
            </GroupRow>
          ))}
        </Group>
      ) : null}

      <View style={styles.desk}>
        <DeskScene
          items={items}
          interactive
          accessibilityLabel={t.desk.label(items.map((item) => t.desk.items[item]))}
        />
        <View style={styles.caption}>
          <ThemedText type="footnote" themeColor="textSecondary" style={styles.shrink}>
            {items.length ? `${t.today.deskTitle} · ${t.today.deskCount(items.length)}` : t.today.deskEmpty}
          </ThemedText>
          {level === 'detailed' ? (
            <ThemedText type="footnote" themeColor="textSecondary" importantForAccessibility="no">
              {t.today.deskTap}
            </ThemedText>
          ) : null}
        </View>
      </View>

      <View style={styles.prompt}>
        <ThemedText type="headline" style={styles.center}>
          {t.today.promptTitle}
        </ThemedText>
        <ThemedText themeColor="textSecondary" style={styles.center}>
          {t.today.promptBody}
        </ThemedText>
        <Button title={t.today.start} onPress={() => router.push('/checkin/task')} style={styles.cta} />
      </View>

      {/* Se ofrece una sola vez y no vuelve a aparecer: la persona elige, sin insistir. */}
      {!settings.experienceOffered ? (
        <Group title={t.today.experienceTitle}>
          <GroupRow first>
            <ThemedText type="callout">{t.today.experienceBody}</ThemedText>
            <Button
              variant="secondary"
              title={t.today.experienceYes}
              onPress={() => update({ details: true, sounds: true, experienceOffered: true })}
            />
            <Button variant="plain" title={t.today.experienceNo} onPress={() => update({ experienceOffered: true })} />
          </GroupRow>
        </Group>
      ) : null}

      {lastHelped ? (
        <Group title={t.today.lastHelped}>
          <GroupRow first>
            <ThemedText type="bodyStrong">{lastHelped.adjustment.title}</ThemedText>
            <ThemedText type="footnote" themeColor="textSecondary">
              {[labels.task(lastHelped.task), lastHelped.space?.name].filter(Boolean).join(' · ')}
            </ThemedText>
          </GroupRow>
        </Group>
      ) : null}

      {trying.isError ? <Notice text={t.common.offline} action={t.common.retry} onAction={refresh} /> : null}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  content: {
    padding: Spacing.three,
    paddingBottom: Spacing.six,
    gap: Spacing.five,
    width: '100%',
    maxWidth: MaxContentWidth,
    alignSelf: 'center',
  },
  desk: {
    gap: Spacing.two,
  },
  caption: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    columnGap: Spacing.two,
    paddingHorizontal: Spacing.one,
  },
  shrink: {
    flexShrink: 1,
  },
  prompt: {
    alignItems: 'center',
    gap: Spacing.three,
  },
  center: {
    textAlign: 'center',
  },
  cta: {
    alignSelf: 'stretch',
  },
});
