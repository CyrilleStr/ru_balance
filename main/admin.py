from django.contrib import admin

from .models import User, Block, BlockChain

admin.site.register(User)
admin.site.register(Block)
admin.site.register(BlockChain)
