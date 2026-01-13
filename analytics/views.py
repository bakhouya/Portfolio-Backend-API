
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status, generics
from django.db.models import Count
from projects.serializers import ProjectSerializer
from visitors.models import Visitor, Visit
from projects.models import Project
from contacts.models import Contact 





# =====================================================================================================
# Get Dashboard Statictics
# =====================================================================================================
class DashboardStatisticsView(APIView):
    # permission_classes = [IsAuthenticated]     
    def get(self, request):
        today = timezone.now().date()

        # Visitors
        visitors = Visitor.objects.count()
        visitors_today = Visitor.objects.filter(first_visit__date=today).count()
        # Visits
        visits = Visit.objects.count()
        visits_today = Visit.objects.filter(visit_date=today).count()
        #  Percentage Visits Today
        visitors_today_percentage = 0
        if visitors > 0:
            visitors_today_percentage = (visits_today  / visitors) * 100       
        # Projects
        all_projects_count = Project.objects.count()
        
        # Pending Contacts Messages
        pending_contacts = Contact.objects.filter(status=False).count()

        
        # Structure Response Data
        statistics = {
            'visitors': {
                'visitors': visitors,
                'visits': visits,
                'visits_today': visits_today,
                'visitors_today': visitors_today,
                'visits_today_percentage': round(visitors_today_percentage, 2),
            },
            'projects': all_projects_count,
            'contacts': pending_contacts
        }

        return Response({'statistics': statistics, 'today': timezone.now()}, status=status.HTTP_200_OK)
# =====================================================================================================
# 
# 
# =====================================================================================================
# Get Statistic Visistis use resource
# =====================================================================================================
class DetailedSourceAnalysisView(APIView):
    def get(self, request):
        try:
            visits = Visit.objects.exclude(referrer__isnull=True).exclude(referrer='')            
            if not visits.exists():
                return Response({'detailed_analysis': [], 'message': "No Data Found" })

            sources_analysis = self.analyze_main_sources(visits)
            detailed_analysis = []
            # biuld detailed analysis with example urls
            for source_data in sources_analysis:
                source_name = source_data['source']
                source_visits = visits.filter(
                    referrer__icontains=self.get_source_domain(source_name)
                ) if source_name != 'direct' else visits.filter(referrer__isnull=True) | visits.filter(referrer='')
                
                # get top referrers with example urls
                source_breakdown = []
                for sub_source_name, sub_data in source_data['details'].items():
                    # get example url for subsource
                    example_url = self.get_example_url_for_subsource(source_visits, source_name, sub_source_name)
                    
                    source_breakdown.append({
                        'type': sub_source_name,
                        'visits': sub_data['visits'],
                        'percentage': sub_data['percentage'],
                        'url': example_url
                    })

                # get source entry
                source_entry = {
                    'type': source_name,
                    'visits': source_data['total_visits'],
                    'percentage': source_data['percentage'],
                    'sources': source_breakdown
                }
                
                detailed_analysis.append(source_entry)
            
            return Response(detailed_analysis, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def analyze_main_sources(self, visits):
        sources = {}
        
        for visit in visits:
            referrer = visit.referrer
            main_source = self.get_main_source(referrer)
            
            if main_source not in sources:
                sources[main_source] = {'total_visits': 0, 'referrers': {}}
            
            sources[main_source]['total_visits'] += 1
            
            sub_source = self.get_sub_source(referrer, main_source)
            if sub_source not in sources[main_source]['referrers']:
                sources[main_source]['referrers'][sub_source] = 0
            sources[main_source]['referrers'][sub_source] += 1
        
        result = []
        for source_name, data in sources.items():
            total = data['total_visits']
            percentage = (total / visits.count()) * 100 if visits.count() > 0 else 0
            details = self.analyze_source_referrers(data['referrers'])            
            result.append({
                'source': source_name,
                'total_visits': total,
                'percentage': round(percentage, 2),
                'details': details
            })
        result.sort(key=lambda x: x['total_visits'], reverse=True)
        return result
    
    def get_main_source(self, referrer):
        if not referrer or 'direct' in referrer.lower():
            return 'direct'
        
        referrer_lower = referrer.lower()
        sources_map = {
            'facebook.com': 'facebook',
            'fb.com': 'facebook',
            'instagram.com': 'instagram',
            'twitter.com': 'twitter',
            'x.com': 'twitter',
            'linkedin.com': 'linkedin',
            'tiktok.com': 'tiktok',
            'youtube.com': 'youtube',
            'google.com': 'google',
            'bing.com': 'bing',
            'yahoo.com': 'yahoo',
        }
        
        for domain, source in sources_map.items():
            if domain in referrer_lower:
                return source
        
        return 'other'
    
    def get_sub_source(self, referrer, main_source):
        referrer_lower = referrer.lower()
        
        if main_source == 'facebook':
            if '/ads/' in referrer_lower or 'utm_campaign=' in referrer_lower:
                return 'ads'
            elif '/groups/' in referrer_lower:
                return 'groups'
            elif '/pages/' in referrer_lower:
                return 'pages'
            elif '/events/' in referrer_lower:
                return 'events'
            elif '/marketplace/' in referrer_lower:
                return 'marketplace'
            else:
                return 'posts'
        
        elif main_source == 'google':
            if '/search' in referrer_lower:
                return 'search'
            elif '/ads/' in referrer_lower:
                return 'ads'
            elif '/maps/' in referrer_lower:
                return 'maps'
            else:
                return 'other'
        
        elif main_source == 'instagram':
            if '/p/' in referrer_lower:
                return 'posts'
            elif '/reel/' in referrer_lower:
                return 'reels'
            elif '/stories/' in referrer_lower:
                return 'stories'
            else:
                return 'other'
        
        elif main_source == 'tiktok':
            if '/video/' in referrer_lower:
                return 'videos'
            elif '/ads/' in referrer_lower:
                return 'ads'
            else:
                return 'other'
        
        elif main_source == 'twitter':
            if '/status/' in referrer_lower:
                return 'tweets'
            elif '/ads/' in referrer_lower:
                return 'ads'
            else:
                return 'other'
        
        elif main_source == 'linkedin':
            if '/feed/' in referrer_lower:
                return 'posts'
            elif '/company/' in referrer_lower:
                return 'company'
            elif '/jobs/' in referrer_lower:
                return 'jobs'
            else:
                return 'other'
        
        elif main_source == 'youtube':
            if '/watch' in referrer_lower:
                return 'videos'
            elif '/channel/' in referrer_lower:
                return 'channels'
            elif '/c/' in referrer_lower:
                return 'creators'
            else:
                return 'other'
        
        return 'general'
    
    def analyze_source_referrers(self, referrers_dict):
        total = sum(referrers_dict.values())
        
        details = {}
        for sub_source, count in referrers_dict.items():
            percentage = (count / total) * 100 if total > 0 else 0
            details[sub_source] = {'visits': count, 'percentage': round(percentage, 2)}
        
        return details
    
    def get_source_domain(self, source_name):
        domains = {
            'facebook': 'facebook.com',
            'google': 'google.com',
            'instagram': 'instagram.com',
            'tiktok': 'tiktok.com',
            'twitter': 'twitter.com',
            'linkedin': 'linkedin.com',
            'youtube': 'youtube.com',
            'bing': 'bing.com',
            'yahoo': 'yahoo.com',
        }
        return domains.get(source_name, source_name)
       
    def get_example_url_for_subsource(self, visits, main_source, sub_source):
        filtered_visits = visits.filter(referrer__isnull=False)

        if main_source == 'facebook':
            if sub_source == 'ads':
                filtered_visits = filtered_visits.filter(referrer__icontains='ads')
            elif sub_source == 'groups':
                filtered_visits = filtered_visits.filter(referrer__icontains='groups')
            elif sub_source == 'pages':
                filtered_visits = filtered_visits.filter(referrer__icontains='pages')
        
        elif main_source == 'google':
            if sub_source == 'search':
                filtered_visits = filtered_visits.filter(referrer__icontains='/search')
            elif sub_source == 'maps':
                filtered_visits = filtered_visits.filter(referrer__icontains='/maps')
        
        elif main_source == 'instagram':
            if sub_source == 'posts':
                filtered_visits = filtered_visits.filter(referrer__icontains='/p/')
            elif sub_source == 'reels':
                filtered_visits = filtered_visits.filter(referrer__icontains='/reel/')
        
        elif main_source == 'tiktok':
            if sub_source == 'videos':
                filtered_visits = filtered_visits.filter(referrer__icontains='/video/')
        
        example = filtered_visits.first()
        if example and example.referrer:
            return example.referrer[:100] 

        default_urls = {
            'facebook': 'https://www.facebook.com/',
            'google': 'https://www.google.com/search',
            'instagram': 'https://www.instagram.com/',
            'tiktok': 'https://www.tiktok.com/',
            'twitter': 'https://twitter.com/',
            'linkedin': 'https://www.linkedin.com/',
            'youtube': 'https://www.youtube.com/',
            'direct': 'Direct Visit',
            'other': 'Other Source'
        }
        
        return default_urls.get(main_source, '')
# =====================================================================================================
# 
# 
# =====================================================================================================
# Get Top Viewed Projects
# =====================================================================================================
class TopViewedProjectsView(generics.ListAPIView):

    serializer_class = ProjectSerializer
    queryset = Project.objects.annotate(views_count=Count('views')).order_by('-views_count')[:10]

    def get(self, request, *args, **kwargs):
        try:
            projects = self.get_queryset()
            serializer = self.get_serializer(projects, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# =====================================================================================================
# 
# 
# =====================================================================================================
# Get Simple Visitors Chart Data for last 7 days 
# =====================================================================================================
class SimpleVisitorsChartView(APIView):
    def get(self, request):
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=6)
        chart_data = []
        
        for i in range(7):
            current_date = start_date + timedelta(days=i)
            
            visitors = Visitor.objects.filter(first_visit__date=current_date).count()
            visits = Visit.objects.filter(visit_date=current_date).count()
            
            chart_data.append({
                'date': current_date.strftime("%Y-%m-%d"),
                'day': current_date.strftime("%A"), 
                'visitors': visitors,
                'visits': visits
            })
        
        total_visitors = sum(item['visitors'] for item in chart_data)
        total_visits = sum(item['visits'] for item in chart_data)

        for item in chart_data:
            if total_visitors > 0:
                item['visitors_percentage'] = round((item['visitors'] / total_visitors) * 100, 2)
            else:
                item['visitors_percentage'] = 0
                
            if total_visits > 0:
                item['visits_percentage'] = round((item['visits'] / total_visits) * 100, 2)
            else:
                item['visits_percentage'] = 0
        
        return Response({
            'period': '7days',
            'dates': [item['date'] for item in chart_data],
            'days': [item['day'] for item in chart_data],
            'visitors': [item['visitors'] for item in chart_data],
            'visits': [item['visits'] for item in chart_data],
        }, status=status.HTTP_200_OK)
# =====================================================================================================
