from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Game, Category, Cart, CartItem, Order, OrderItem
from decimal import Decimal
from .forms import UserRegisterForm
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from django.core.paginator import Paginator

def home(request):
    # Get featured games (you can customize this logic)
    featured_games = Game.objects.filter(is_featured=True)[:6]
    
    # Get latest games
    latest_games = Game.objects.order_by('-release_date')[:8]
    
    # Get discounted games
    discounted_games = Game.objects.filter(discount__gt=0)[:3]
    
    # Get all categories
    categories = Category.objects.all()
    
    context = {
        'featured_games': featured_games,
        'latest_games': latest_games,
        'discounted_games': discounted_games,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)

def game_list(request):
    # Get all games
    games = Game.objects.all()
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        games = games.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Category filter
    categories = request.GET.getlist('category')
    if categories:
        games = games.filter(category__slug__in=categories)
    
    # Price range filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        games = games.filter(price__gte=min_price)
    if max_price:
        games = games.filter(price__lte=max_price)
    
    # Sort
    sort = request.GET.get('sort', 'newest')
    if sort == 'newest':
        games = games.order_by('-release_date')
    elif sort == 'price_asc':
        games = games.order_by('price')
    elif sort == 'price_desc':
        games = games.order_by('-price')
    elif sort == 'name_asc':
        games = games.order_by('title')
    elif sort == 'name_desc':
        games = games.order_by('-title')
    
    # Pagination
    paginator = Paginator(games, 12)  # Show 12 games per page
    page = request.GET.get('page')
    games = paginator.get_page(page)
    
    # Get all categories for the filter sidebar
    categories = Category.objects.all()
    
    context = {
        'games': games,
        'categories': categories,
    }
    return render(request, 'store/game_list.html', context)

def game_detail(request, slug):
    game = get_object_or_404(Game, slug=slug)
    related_games = Game.objects.filter(category=game.category).exclude(id=game.id)[:4]
    
    context = {
        'game': game,
        'related_games': related_games,
    }
    return render(request, 'store/game_detail.html', context)

def get_cart(request):
    """Get the current cart from session or create a new one."""
    cart = request.session.get('cart', {})
    return cart

def get_cart_items(request):
    """Get cart items with game details."""
    cart = get_cart(request)
    items = []
    subtotal = Decimal('0.00')
    
    for game_id, quantity in cart.items():
        game = get_object_or_404(Game, id=game_id)
        item_total = game.price * quantity
        subtotal += item_total
        items.append({
            'game': game,
            'quantity': quantity,
            'total': item_total
        })
    
    tax = subtotal * Decimal('0.10')  # 10% tax
    total = subtotal + tax
    
    return items, subtotal, tax, total

@require_http_methods(["GET"])
def cart(request):
    """Display the shopping cart."""
    items, subtotal, tax, total = get_cart_items(request)
    
    context = {
        'items': items,
        'subtotal': subtotal,
        'tax': tax,
        'total': total
    }
    return render(request, 'store/cart.html', context)

@login_required
def add_to_cart(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, game=game)
    
    if not created:
        # Check if adding one more would exceed stock
        if cart_item.quantity + 1 <= game.stock:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f'Added another copy of {game.title} to your cart.')
        else:
            messages.error(request, f'Sorry, only {game.stock} copies of {game.title} are available.')
    else:
        messages.success(request, f'Added {game.title} to your cart.')
    
    return redirect('store:cart')

@require_http_methods(["POST"])
def update_cart(request, game_id):
    """Update the quantity of a game in the cart."""
    game = get_object_or_404(Game, id=game_id)
    cart = get_cart(request)
    game_id = str(game_id)
    
    try:
        data = json.loads(request.body)
        action = data.get('action')
        
        if game_id in cart:
            if action == 'increase':
                cart[game_id] += 1
            elif action == 'decrease':
                cart[game_id] -= 1
                if cart[game_id] <= 0:
                    del cart[game_id]
            
            request.session['cart'] = cart
            
            return JsonResponse({
                'success': True,
                'quantity': cart.get(game_id, 0),
                'cart_count': sum(cart.values())
            })
    except json.JSONDecodeError:
        pass
    
    return JsonResponse({'success': False})

@require_http_methods(["POST"])
def remove_from_cart(request, game_id):
    """Remove a game from the cart."""
    cart = get_cart(request)
    game_id = str(game_id)
    
    if game_id in cart:
        del cart[game_id]
        request.session['cart'] = cart
    
    return JsonResponse({
        'success': True,
        'cart_count': sum(cart.values())
    })

@login_required
def checkout(request):
    """Process the checkout and create an order."""
    items, subtotal, tax, total = get_cart_items(request)
    
    if not items:
        messages.warning(request, 'Your cart is empty!')
        return redirect('store:cart')
    
    # Create order
    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        total_amount=total
    )
    
    # Create order items
    for item in items:
        OrderItem.objects.create(
            order=order,
            game=item['game'],
            quantity=item['quantity'],
            price=item['game'].price
        )
    
    # Clear the cart
    request.session['cart'] = {}
    
    messages.success(request, 'Order placed successfully!')
    return redirect('store:order_confirmation', order_id=order.id)

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('accounts:login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@require_http_methods(["GET"])
def cart_count(request):
    """Return the current number of items in the cart."""
    cart = request.session.get('cart', {})
    count = sum(cart.values())
    return JsonResponse({'count': count})

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_confirmation.html', {'order': order})
