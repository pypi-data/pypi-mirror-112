
class MeerkatEvents:
    def onMessageEvent(self, event):
        @self.meerkat.event
        async def on_message(message):
            await event(message)
            await self.meerkat.process_commands(message)

    def bulkOn(self, events):
        if type(events) != list:
            raise Exception(
                'Verify you are sending (name, event)[] to MeerkatBot <bulkOn> method, these are required arguments.'
            )
        for event in events:
            name, event = event
            self.on(name, event, False)

    def on(self, name=None, event=None, end=True):
        if type(name) != str or not callable(event):
            raise Exception(
                'Verify you are sending name and event to MeerkatBot <on> method, these are required arguments.'
            )
        event.__name__ = "on_" + name
        if name == 'message':
            self.onMessageEvent(event)
        else:
            self.meerkat.event(event)
        if end:
            return self
