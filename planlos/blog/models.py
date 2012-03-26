from django.db import models
import datetime

# Create your models here.
class Entry(models.Model):
    pub_date = models.DateTimeField(default=datetime.datetime.now, blank=True)
    title = models.CharField(max_length=40)
    content = models.TextField()
    author = models.CharField(max_length=40)

    def __unicode__(self):
        return self.title+ " "+str(self.pub_date)


    def save(self, **kwargs):
        """override save to set defaults""" 
        #print "Saving...."
        self.pub_date = datetime.datetime.now()
        super(Entry, self).save(**kwargs)

