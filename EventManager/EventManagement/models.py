from django.db import models


class Resgistration(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    eventid_event = models.ForeignKey('Event', models.DO_NOTHING, db_column='EventID_Event')  # Field name made lowercase.
    date = models.IntegerField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    waspresent = models.IntegerField(db_column='WasPresent', blank=True, null=True)  # Field name made lowercase.
    participantuserid = models.ForeignKey(Participante, models.DO_NOTHING, db_column='ParticipantUserID')  # Field name made lowercase.

def cancelregistrations(self) :
    Answer.objects.filter(Registrationid_answer=id_registrations , participantuserid_registrations=id.authUser).delete()
    return redirect('home.html')


    class Meta:
        
        db_table = 'resgistration'