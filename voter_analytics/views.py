from django.shortcuts import render
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter 
import plotly
import plotly.graph_objs as go
# Create your views here.

class VoterListView(ListView):
    '''View to display all voter analytics'''

    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100       #show 100 voters on 1 page

    def get_context_data(self):
        '''overriding to provide the options in the search feature'''
        context = super().get_context_data()

        parties = Voter.objects.values('party').distinct()
        partyList = []
        for party in parties:
            partyList.append(party['party'])

        birthDays = Voter.objects.values('dob__year').distinct()
        birthYears = []
        for birthDay in birthDays:
            date = birthDay['dob__year']
            birthYears.append(date)
        birthYears.sort()

        voterScores = Voter.objects.values('voter_score').distinct()
        scores = []
        for voterScore in voterScores:
            scores.append(voterScore['voter_score'])
        scores.sort()

        context['parties'] = partyList
        context['birthYears'] = birthYears
        context['voterScores'] = scores

        # Add selected parameters to context
        context['selected_party'] = self.request.GET.get('partyA', '')
        context['selected_min_year'] = self.request.GET.get('minYear', '')
        context['selected_max_year'] = self.request.GET.get('maxYear', '')
        context['selected_voter_score'] = self.request.GET.get('voterScore', '')
        
        # Checkbox persistence
        context['v20_state_checked'] = 'v20_state' in self.request.GET
        context['v21_town_checked'] = 'v21_town' in self.request.GET
        context['v21_primary_checked'] = 'v21_primary' in self.request.GET
        context['v22_general_checked'] = 'v22_general' in self.request.GET
        context['v23_town_checked'] = 'v23_town' in self.request.GET

        return context
    
    def get_queryset(self):
        '''function which will allow the filtering feature
        to work'''

        voters = super().get_queryset()

        if 'partyA' in self.request.GET:
            partyA = self.request.GET['partyA']
            if partyA:
                voters = voters.filter(party = partyA)

        if 'minYear' in self.request.GET:
            minYear = self.request.GET['minYear']
            if minYear:
                voters = voters.filter(dob__year__gte = minYear)

        if 'maxYear' in self.request.GET:
            maxYear = self.request.GET['maxYear']
            if maxYear:
                voters = voters.filter(dob__year__lte = maxYear)

        if 'voterScore' in self.request.GET:
            voterScore = self.request.GET['voterScore']
            print(f'filtering by voter score: {voterScore}')
            if voterScore:
                voters = voters.filter(voter_score = voterScore)

        if 'v20_state' in self.request.GET:
            voters = voters.filter(v20_state = "TRUE")
        if 'v21_town' in self.request.GET:
            voters = voters.filter(v21_town="TRUE")
        if 'v21_primary' in self.request.GET:
            voters = voters.filter(v21_primary="TRUE")
        if 'v22_general' in self.request.GET:
            voters = voters.filter(v22_general="TRUE")
        if 'v23_town' in self.request.GET:
            voters = voters.filter(v23_town="TRUE")
        
        return voters
    

class VoterDetailView(DetailView):
    '''View to show details on a single voter'''

    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'v'

class GraphListView(ListView):
    '''a view to show graphs about voter analytics'''

    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = "v"

    def get_context_data(self, **kwargs):
        '''Provide context variables for template, builds graphs'''

        context = super().get_context_data(**kwargs)
        v = context('v')

        #bar chart for birth years
        allYearsQuery = Voter.objects.values('dob__year').distinct()
        years = []
        for year in allYearsQuery:
            years.append(year['dob__year'])


