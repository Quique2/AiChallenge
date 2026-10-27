import { router } from 'expo-router';

import { Button } from '@/components/button';
import { DeskScene } from '@/components/desk/desk-scene';
import { StepScreen } from '@/components/step-screen';
import { useT } from '@/i18n';
import { useDesk } from '@/lib/desk';

/** Al aceptar un ajuste, la onda del monitor se calma: el entorno que se acomoda. */
export default function Done() {
  const t = useT();
  const desk = useDesk();
  return (
    <StepScreen
      title={t.reminder.doneTitle}
      hint={t.reminder.doneBody}
      footer={<Button title={t.common.backToToday} onPress={() => router.dismissTo('/today')} />}>
      <DeskScene
        items={desk.items}
        settle
        accessibilityLabel={t.desk.label(desk.items.map((item) => t.desk.items[item]))}
      />
    </StepScreen>
  );
}
