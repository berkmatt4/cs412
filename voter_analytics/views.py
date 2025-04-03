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

        #getting all of the options for political parties to display
        # as options for the search bar
        parties = Voter.objects.values('party').distinct()
        partyList = []
        for party in parties:
            partyList.append(party['party'])

        #getting all distinct birth years to display on search bar
        birthDays = Voter.objects.values('dob__year').distinct()
        birthYears = []
        for birthDay in birthDays:
            date = birthDay['dob__year']
            birthYears.append(date)
        birthYears.sort()

        #get all voter scores
        voterScores = Voter.objects.values('voter_score').distinct()
        scores = []
        for voterScore in voterScores:
            scores.append(voterScore['voter_score'])
        scores.sort()

        #add these to the context variables
        context['parties'] = partyList
        context['birthYears'] = birthYears
        context['voterScores'] = scores

        #currently selected stuff needs to be context too
        #this ensures persistence upon page reload
        context['selected_party'] = self.request.GET.get('partyA', '')
        context['selected_min_year'] = self.request.GET.get('minYear', '')
        context['selected_max_year'] = self.request.GET.get('maxYear', '')
        context['selected_voter_score'] = self.request.GET.get('voterScore', '')
        
        #same as above but for checkboxes
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

        #If we have a filter for political party, filter the query
        if 'partyA' in self.request.GET:
            partyA = self.request.GET['partyA']
            if partyA:
                voters = voters.filter(party = partyA)

        #if we have a filter for min birth year, filter by all 
        #people born in year >= that year
        if 'minYear' in self.request.GET:
            minYear = self.request.GET['minYear']
            if minYear:
                voters = voters.filter(dob__year__gte = minYear)

        #same with minYear, except this time <= that year
        if 'maxYear' in self.request.GET:
            maxYear = self.request.GET['maxYear']
            if maxYear:
                voters = voters.filter(dob__year__lte = maxYear)

        #filtering for voter score, further refining query results
        if 'voterScore' in self.request.GET:
            voterScore = self.request.GET['voterScore']
            print(f'filtering by voter score: {voterScore}')
            if voterScore:
                voters = voters.filter(voter_score = voterScore)

        #filtering for checkboxes
        #if these exist in the request, then they were checked and must
        #filter the results as such
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

class GraphListView(VoterListView):
    '''a view to show graphs about voter analytics
    I made it so this inherits from VoterListView, rather than
    the generic list view. This way I could re-use my filtering of the
    queryset without re-writing everything'''

    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = "v"

    
    def get_context_data(self, **kwargs):
        '''Provide context variables for template, builds graphs'''

        context = super().get_context_data(**kwargs)
        #call get_queryset of VoterListView
        filtered_voters = self.get_queryset()

        #bar chart for birth years
        years = filtered_voters.values("dob__year").distinct()
        yearList = []
        
        #get all distinct years
        for year in years:
            yearList.append(year['dob__year'])
        yearList.sort()

        #now, for each distinct year, if you see that year in the 
        #query of all years, increase that year's count by 1
        #list indices are corresponding
        allYears = filtered_voters.values('dob__year')
        yearCount = [0] * len(yearList)
        for j in range(len(yearList)):
            for i in range(len(allYears)):
                if yearList[j] == allYears[i]['dob__year']:
                    yearCount[j] += 1

        #construct the histogram
        yearHistogram = go.Bar(
            x = yearList,
            y = yearCount,
            name = "Birth Years"
        )

        #display it as context with a div
        layout = go.Layout(title = 'Voters by Birth Year')
        figure = go.Figure(data = [yearHistogram], layout=layout)
        context['birth_year_plot'] = plotly.offline.plot(figure, output_type = 'div')


        #now get all distinct parties
        parties = filtered_voters.values('party').distinct()
        partyList = []
        for party in parties:
            partyList.append(party['party'])

        allParties = filtered_voters.values('party')
        partyCount = [0] * len(partyList)

        #for each party in the whole queryset, add 1 to the
        #corresponding index
        for i in range(len(partyList)):
            for j in range(len(allParties)):
                if partyList[i] == allParties[j]['party']:
                    partyCount[i] += 1

        #construct the pie chart
        party_pie = go.Pie(
            labels = partyList,
            values = partyCount,
            name = "Party Affiliation"
        )

        #return context as a div
        layout = go.Layout(title = "Voter Party Affiliation")
        figure = go.Figure(data=[party_pie], layout=layout)
        context['party_plot'] = plotly.offline.plot(figure, output_type = 'div')

        #list of all elections
        elections = ['v20_state', 'v21_town', 'v21_primary', 'v22_general', 'v23_town']
        electionCounts = [0] * len(elections)

        #grab the length of each queryset
        #this will represent the number of people who voted in each
        electionCounts[0] = len(filtered_voters.filter(v20_state = "TRUE"))
        electionCounts[1] = len(filtered_voters.filter(v21_town = "TRUE"))
        electionCounts[2] = len(filtered_voters.filter(v21_primary = "TRUE"))
        electionCounts[3] = len(filtered_voters.filter(v22_general = "TRUE"))
        electionCounts[4] = len(filtered_voters.filter(v23_town = "TRUE"))

        #construct the histogram
        election_counts = go.Bar(
            x = elections,
            y = electionCounts,
            name = 'Election Participation'
        )
        #display it as context with a div
        layout = go.Layout(title = "Voter Participation by Election")
        figure = go.Figure(data = [election_counts], layout=layout)
        context['election_plot'] = plotly.offline.plot(figure, output_type = 'div')



        return context
            

        
            
            


