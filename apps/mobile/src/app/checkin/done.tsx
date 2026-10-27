import { router } from 'expo-router';
import { useEffect } from 'react';

import { Button } from '@/components/button';
import { DeskScene, SETTLED_MS } from '@/components/desk/desk-scene';
import { StepScreen } from '@/components/step-screen';
import { useT } from '@/i18n';
import { useDesk } from '@/lib/desk';
import { useFeedback } from '@/lib/feedback';

/**
 * Al aceptar un ajuste, la onda del monitor se calma: el entorno que se acomoda. El sonido y la
 * vibración de confirmar llegan en el cuadro en que la onda queda tranquila.
 */
export default function Done() {
  const t = useT();
  const desk = useDesk();
  const feedback = useFeedback();

  useEffect(() => {
    const timer = setTimeout(feedback.confirm, SETTLED_MS);
    return () => clearTimeout(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps -- solo al llegar a la pantalla
  }, []);
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
