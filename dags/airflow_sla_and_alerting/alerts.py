from advanced_airflow_concepts.slack_hook import SlackWebhookImpl


class AlertManager:

    @staticmethod
    def on_failure_callback(context):
        text = ':large_red_circle: %s task failed' % str(context['task_instance'])
        AlertManager.post(text=text)

    @staticmethod
    def on_retry_callback(context):
        text = ':large_blue_circle: %s task retry' % str(context['task_instance'])
        AlertManager.post(text=text)

    @staticmethod
    def on_success_callback(context):
        text = ':large_green_circle: %s task success' % str(context['task_instance'])
        AlertManager.post(text=text)

    @staticmethod
    def sla_miss_callback(context):
        text = ':large_red_circle: %s sla miss' % str(context['task_instance'])
        AlertManager.post(text=text)

    @staticmethod
    def post(text):
        hook = SlackWebhookImpl(text=text, url='...')
        hook.execute()
