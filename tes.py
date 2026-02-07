from contentful import Client


client = Client(
    'w6sn00a0nw61',
    'sXe4bg57oay8cu-2MFzjoF6o3F-lH4va_r4DaK3hIFw',
    environment='master'  # Optional - it defaults to 'master'.
)

# entries = client.entries()
# items = []
# for entry in entries:
#     id = entry.id
#     print(id)

# res = client.entries({
#     # content_type: 'BlogPost',
#     'limit': 1,
#     # 'skip': 10,
#     'order': '-sys.createdAt',
#     'sys.publishedAt[lt]': '2026-02-01'
# })

next_entries = client.entries({
    'content_type': 'blogPost',
    'fields.date[lt]': '2026-02-01',
    'order': '-fields.date',
    'limit': 1
})

for e in next_entries:
    print(e.date, e.title)