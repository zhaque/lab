"""Set up for Django admin.

"""

from mashapp.models import *
from django.contrib import admin


class SolrFieldInline(admin.TabularInline):
    model = SolrField
    extra = 5

class SolrHandlerConfigAdmin(admin.ModelAdmin):
    inlines = [SolrFieldInline]
#    exclude = ['name']

admin.site.register(SolrHandlerConfig, SolrHandlerConfigAdmin)


    
class MashupAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, 
         {'fields': ['title', 'solr_handler_config']}),
#        ('[External]  Common BOSS options', 
#         {'description': 'See: http://developer.yahoo.com/search/boss/boss_guide/univer_api_args.html',
#          'fields': ['BOSS_sites', 'BOSS_lang', 'BOSS_region'], 'classes': ['collapse']}),
#        ('[External]  BOSS web search options', 
#         {'description': 'See: http://developer.yahoo.com/search/boss/boss_guide/Web_Search.html#optional_args_web',
#          'fields': ['BOSS_web_enabled', 'BOSS_web_abstract', 'BOSS_web_filter'], 'classes': ['collapse']}),
#        ('[External]  BOSS images search options', 
#         {'description': 'See: http://developer.yahoo.com/search/boss/boss_guide/Submit_Image_Queries.html#optional_args_image',
#          'fields': ['BOSS_images_enabled', 'BOSS_images_filter', 'BOSS_images_dimensions'], 'classes': ['collapse']}),
#        ('[External]  BOSS news search options', 
#         {'description': 'See http://developer.yahoo.com/search/boss/boss_guide/News_Search.html#optional_args_news',
#          'fields': ['BOSS_news_enabled', 'BOSS_news_filter', 'BOSS_news_age'], 'classes': ['collapse']}),

        ('[External]  Common Google Search options', 
         {'description': 'http://code.google.com/apis/ajaxsearch/documentation/reference.html#_intro_fonje',
          'fields': ['google_search_HL', ], 'classes': ['collapse']}),
        ('[External]  Google Web Search options', 
         {'description': 'See http://code.google.com/apis/ajaxsearch/documentation/reference.html#_fonje_web',
          'fields': ['google_web_enabled', 'google_web_safe', 'google_web_LR', ], 'classes': ['collapse']}),
        ('[External]  Google Image Search options', 
         {'description': 'See http://code.google.com/apis/ajaxsearch/documentation/reference.html#_fonje_image',
          'fields': ['google_image_enabled', 'google_image_safe', 'google_image_imgsz', 'google_image_imgc', 'google_image_imgtype', 'google_image_as_filetype', 'google_image_as_sitesearch', ], 'classes': ['collapse']}),
        ('[External]  Google News Search options', 
         {'description': 'See http://code.google.com/apis/ajaxsearch/documentation/reference.html#_fonje_news',
          'fields': ['google_news_enabled', 'google_news_scoring', 'google_news_geo', 'google_news_qsid', 'google_news_topic', 'google_news_ned',], 'classes': ['collapse']}),
        ('[External]  Google Blog Search options', 
         {'description': 'See http://code.google.com/apis/ajaxsearch/documentation/reference.html#_fonje_blog',
          'fields': ['google_blog_enabled', 'google_blog_scoring'], 'classes': ['collapse']}),
        ('[External]  Google Video Search options', 
         {'description': 'See http://code.google.com/apis/ajaxsearch/documentation/reference.html#_fonje_video',
          'fields': ['google_video_enabled', 'google_video_scoring'], 'classes': ['collapse']}),
#        ('[External]  Picasa Web Search options', 
#         {'description': 'http://code.google.com/apis/picasaweb/reference.html#Parameters',
#          'fields': ['picasa_web_enabled'], 'classes': ['collapse']}),

        
#        ('[External]  Twitter search options', 
#         {'description': 'See http://apiwiki.twitter.com/Search+API+Documentation#Search',
#          'fields': ['twitter_enabled', 'twitter_lang'], 'classes': ['collapse']}),

        ('[External]  Delicious search options', 
         {'description': 'See http://delicious.com/help/feeds',
          'fields': ['delicious_popular_enabled', 'delicious_recent_enabled', 'delicious_markup'], 'classes': ['collapse']}),
        
#        ('[External]  Freebase search options', 
#         {'description': 'See http://www.freebase.com/view/en/api_service_search',
#          'fields': ['freebase_enabled', 'freebase_type', 'freebase_type_strict', 'freebase_domain', 'freebase_domain_strict'], 'classes': ['collapse']}),
#        
#        ('[External]  Amazon search options', 
#         {'description': 'See http://docs.amazonwebservices.com/AWSEcommerceService/2005-02-23/ApiReference/ItemSearchOperation.html',
#          'fields': ['amazon_enabled', 'amazon_search_index'], 'classes': ['collapse']}),
#        
#        ('[External]  Technorati search options', 
#         {'description': 'See http://technorati.com/developers/api/search.html',
#          'fields': ['technorati_enabled', 'technorati_lang', 'technorati_authority', 'technorati_claim'], 'classes': ['collapse']}),
#        
        ('[Internal]  Solr search options', 
         {'description': '',
          'fields': ['twitter_solr_enabled', 
#                     'vertical_solr_enabled',
#                     'wiki_enabled'
                     ], 'classes': ['collapse']}),
        ]
    



admin.site.register(Mashup, MashupAdmin)
