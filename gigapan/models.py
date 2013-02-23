from django.db import models
from taggit.managers import TaggableManager
import json

# Create your models here.

class Issue(models.Model): 
    name        = models.CharField(max_length=200)
    description = models.TextField()
    updated     = models.DateTimeField('date published')

class Eyegore(models.Model):
    gigapan_id  = models.IntegerField()
    foregroundposition= models.CharField(max_length=200)
    foregroundcolor= models.CharField(max_length=200)
    foregroundfocus= models.CharField(max_length=200)
    backgroundcolor= models.CharField(max_length=200)
    numerosity= models.CharField(max_length=200)
    backgroundfocus= models.CharField(max_length=200)
    composition= models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


    def new_from_json(self, gigapan_data):
        print "in new_from_json: ", gigapan_data['gigapan_id']
        f  = Eyegore.objects.filter(gigapan_id=gigapan_data['gigapan_id'])
        if f:
            return
        print "in new_from_json", gigapan_data
        self.gigapan_id = gigapan_data['gigapan_id']
        self.foregroundposition=gigapan_data['foregroundposition']
        self.foregroundcolor=gigapan_data['foregroundcolor']
        self.foregroundfocus=gigapan_data['foregroundfocus']
        self.backgroundcolor=gigapan_data['backgroundcolor']
        self.numerosity=gigapan_data['numerosity']
        self.backgroundfocus=gigapan_data['backgroundfocus']
        self.composition=gigapan_data['composition']
        self.save()

class Gallery(models.Model):
    gallery_id  = models.IntegerField('Gallery id on gigapan.org')
    name        = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner      = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name	

    def new_from_json(self, gallery_data):
        f  = Gallery.objects.filter(gallery_id=gallery_data['gallery_id'])
        if f:
            # this gallery exists
            print "\tfound this gallery, returning with no action"
            return
        print "start of Gallery.new_from_json()"
        self.gallery_id  = gallery_data['gallery_id']
        self.name        = gallery_data['name']
        self.description = gallery_data['description']
        self.owner = gallery_data['owner']
        self.save()


	
class Gigapan(models.Model):
	gigapan_id  = models.IntegerField()
	owner_id    = models.IntegerField()
	name        = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	taken		= models.DateTimeField('date taken', blank=True, null=True)
	uploaded    = models.DateTimeField('date uploaded')
	updated     = models.DateTimeField('date updated')
	height      = models.IntegerField()
	width       = models.IntegerField()
	gigapixels  = models.IntegerField()
	levels      = models.IntegerField()
	aspect		= models.FloatField(blank=True, null=True)
	
	stitcher_notes = models.TextField(blank=True)
	#created_at	= models.DateTimeField('date created')
	# geolocation parameters
	latitude    = models.FloatField(blank=True, null=True)
	longitude   = models.FloatField(blank=True, null=True)
	roll   		= models.FloatField(blank=True, null=True)
	altitude   	= models.FloatField(blank=True, null=True)
	heading		= models.FloatField(blank=True, null=True)
	tilt		= models.FloatField(blank=True, null=True)
	distance	= models.FloatField(blank=True, null=True)
	field_of_view_w  = models.FloatField(blank=True, null=True)
	field_of_view_h  = models.FloatField(blank=True, null=True)
	field_of_view_b  = models.FloatField(blank=True, null=True)
	tags = TaggableManager()
	galleries	= models.ManyToManyField(Gallery)

	# TODO: add update_from_json(slef, gigapan_data)
	
	def __unicode__(self):
		return self.name


	def new_from_json(self, gigapan_data):
		f  = Gigapan.objects.filter(gigapan_id=gigapan_data['gigapan_id'])
		if f:
			return
		self.gigapan_id = gigapan_data['gigapan_id']
		self.name        = gigapan_data['name']
		self.owner_id    = gigapan_data['owner']['id']
		self.description = gigapan_data['description']
		self.uploaded    = gigapan_data['uploaded']
		self.updated     = gigapan_data['updated']
		self.height      = gigapan_data['height']
		self.width       = gigapan_data['width']
		self.gigapixels  = gigapan_data['gigapixels']
		self.levels      = gigapan_data['levels']
		self.aspect = float(gigapan_data['width'])/gigapan_data['height']
		if (gigapan_data['location']):
			self.latitude  = gigapan_data['location']['latitude']
			self.longitude = gigapan_data['location']['longitude']
		self.save()
		if gigapan_data['tag_set']:
			for tag in gigapan_data['tag_set']:
				self.tags.add(tag)
		print gigapan_data['name']

	# load from gigapan/<gigapan_id>.json files
	def new_from_new_json(self, gigapan_data):
		f  = Gigapan.objects.filter(gigapan_id=gigapan_data['gigapan_id'])
		if f:
			f[0].taken   = gigapan_data['taken_at']
			f[0].updated = gigapan_data['updated_at']
			f[0].created = gigapan_data['created_at']
			f[0].save()
			
			return
			# this gigapan exists...I don't know how to update it more elegantly.
			
		self.gigapan_id = gigapan_data['gigapan_id']
		self.name        = gigapan_data['name']
		if (gigapan_data['user_id']):
			self.owner_id	 = gigapan_data['user_id']
		#		if (gigapan_data['owner']):        
		#			self.owner_id    = gigapan_data['owner']['id']
		self.description = gigapan_data['description']
		#self.taken       = gigapan_data['taken']
		self.taken       = gigapan_data['taken_at']
	
		#self.uploaded    = gigapan_data['uploaded']
		self.uploaded    = gigapan_data['created_at']
		self.updated     = gigapan_data['updated_at']
		self.height      = gigapan_data['height']
		self.width       = gigapan_data['width']
		#		self.gigapixels  = gigapan_data['gigapixels']
		self.gigapixels  = gigapan_data['resolution']/1000000000
		self.aspect = float(gigapan_data['width'])/gigapan_data['height']
	
		self.levels      = gigapan_data['levels']
		#if (gigapan_data['location']):
		#if (gigapan_data['is_geolocated']):
		#	self.latitude  = gigapan_data['location']['latitude']
		#	self.longitude = gigapan_data['location']['longitude']
		#else:
		self.latitude  	= gigapan_data['latitude'] 
		self.longitude 	= gigapan_data['longitude']
		self.roll		= gigapan_data['roll']
		self.altitude = gigapan_data['altitude']
		self.heading = gigapan_data['heading']
		self.tilt = gigapan_data['tilt']
		self.distance = gigapan_data['distance']
		self.field_of_view_w = gigapan_data['field_of_view_w']
		self.field_of_view_h = gigapan_data['field_of_view_h']
		self.field_of_view_b = gigapan_data['field_of_view_b']
	
		if gigapan_data['stitcher_notes']:
			self.stitcher_notes = gigapan_data['stitcher_notes']
		else:		
			self.stitcher_notes = ''
		
		self.save()

		#if gigapan_data['tag_set']:            
		#	for tag in gigapan_data['tag_set']:
		#		print "in tag loop in Gigapan.new_from_json() tag: %s" % tag
		#		print "tags.add is broken?"
		#		self.tags.add(tag) 
		print "done with Gigapan.new_from_json()"
		print gigapan_data['name']
		
class User(models.Model):
	gigapan_user_id  = models.IntegerField() # same as owner_id
	owner_id    = models.IntegerField()
	username    = models.CharField(max_length=200)
	first_name  = models.CharField(max_length=200)
	last_name   = models.CharField(max_length=200)		
	
	def new_from_json(self, data):
		u  = User.objects.filter(username=data['username'])
		if u:
			return
		self.gigapan_user_id = data['id']
		self.name       = gigapan_data['name']
		self.first_name = data['first_name']
		self.last_name  = data['last_name']

		self.save()
