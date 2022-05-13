# Jitsu_v02

starting from scratch, hopefully with tests

TODO:
1. directory structure
    1. pytest(s)
    2. models
2. steps
    1. check for new mail in [Supplier/InvoicesNew] folder
    2. for each new message
        1. download new mail as Raw
        2. extract email data that will be entered in database
            1. supplier
            2. date
            3. raw email
        3. upload data to postgresql database
        4. on successful extraction and upload move the email out of [Supplier/InvoiceNew] to [Supplier/InvoiceProcessed]
        5. on failed extraction or upload notify admin
    3. convert raw email to invoice/s
        1. formats:
            1. pdf (most suppliers)
            2. html (coca-cola)
            3. csv (BidFood)
        2. extract data in pdf, html, csv into usable information using invoice2data
        3. handle multiple invoice email attachments (JapanFoodCorp)
        4. handle multiple page invoices (TokyoFoodCorp)
        5. match .yml supplier identifier
            1. if none, notify admin
        6. match invoice entry item to jitsu_item
            1. if none found notify admin to either:
                1. correct the entry relationship
                2. add the jitsu_item
