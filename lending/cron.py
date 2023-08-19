import kronos


@kronos.register("0 8 * * *")
def process_scheduled_payments():
    pass
