from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())
# Create your models here.

class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    highlighted = models.TextField()
    class Meta:
        ordering = ('created',)
    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = self.linenos and 'table' or False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)        


class Transaction(models.Model):
    abstract = models.CharField(
    max_length=20,
    verbose_name=(u'摘要'),
    )
    class Manager(models.Manager):
        def get_queryset(self):
            print(super(self.__class__, self)) 
            query_set = super(self.__class__, self).get_queryset()
            return super(self.__class__, self).get_queryset().filter(id=1)
    objects = Manager() 

class Sub(models.Model):
    code = models.CharField(  # required
        max_length=255,
        unique=True,
        verbose_name=(u'编号'),
    )

    tran = models.ForeignKey(
        Transaction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=(u'事务'),        
    )

class testquery(models.Model):
    name = models.CharField(  # required
        default=None,
        max_length=255,
        unique=True,
        verbose_name=(u'名称'),
    )    
    code = models.CharField(  # required
        max_length=255,
        unique=True,
        verbose_name=(u'编号'),
    )
    deleted = models.BooleanField(  # required
        default=False,
        verbose_name=(u'删除状态'),
    )    
    class undeletedManager(models.Manager):
        def get_queryset(self):
            return super(testquery.undeletedManager,self).get_queryset().filter(deleted=False)
    objects_undeleted = undeletedManager()

