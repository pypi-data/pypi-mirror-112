class MeerkatExceptions:

    def badFormedMeerkatInstance():
        raise Exception(
            'Verify you are sending token and prefix keyword variables to MeerkatBot <constructor>, these are required arguments.'
        )

    def badFormedCommandUse():
        raise Exception(
            'Verify you are sending .use(name=str, command=async function) to MeerkatBot <use>, these are required arguments.'
        )

    def badFormedCommandBulkUse():
        raise Exception(
            'Verify you are sending (name=str, command=async function) to MeerkatBot <bulkUse> method [(name, command), (name,command)], these are required arguments.'
        )

    def badFormedEventOn():
        raise Exception(
            'Verify you are sending .on(name=str, event=async function) to MeerkatBot <on> method, these are required arguments.'
        )

    def badFormedEventBulkOn():
        raise Exception(
            'Verify you are sending (name=str, event=async function) to MeerkatBot <bulkOn> method [(name, event), (name,event)], these are required arguments.'
        )
