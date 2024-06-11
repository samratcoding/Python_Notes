# Here are example views.py of bulk keyword posting
# If request is fetch() or ajax then return JSON
# Otherwise return template view


from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def bulk_posting(request):
        curent_user = request.user
        website = Website_List.objects.filter(user=curent_user)
        youtubeapi = Youtube_api.objects.filter(user=curent_user)
        keyword_pending = info_bulk_model.objects.filter(user=curent_user, status='Pending')
        running_keyword = info_bulk_model.objects.filter(user=curent_user, status='Running')
        keyword_completed = info_bulk_model.objects.filter(user=curent_user, status='Completed')
        keyword_faild = info_bulk_model.objects.filter(user=curent_user, status='Failed')

        # When url call is normal then render template when call is js fetch then return JSON for page update
        # Here pending_keywords.html and running_keywords.html are part of posting in seperate to dynamically update data part
        data = {
            'keyword_pending': render_to_string('pending_keywords.html', {'keyword_pending': keyword_pending}),
            'running_keyword': render_to_string('running_keywords.html', {'running_keyword': running_keyword}),
        }

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            print("Returning JSON response")
            return JsonResponse(data)
        else:
            print("Rendering HTML template")
            template = 'infoapp/bulk/posting.html'
            context = {'keyword_pending': keyword_pending, 'youtubeapi': youtubeapi,
                    'website': website, 'keyword_completed': keyword_completed,
                    'keyword_faild': keyword_faild,
                    'running_keyword': running_keyword
                    }
            return render(request, template, context=context)
