from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
# Create your views here.
from game.models import Game
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User

from .serializers import (
                        BetSerializer,
                        CartSerializer,
                        ContestSerializer,
                        GameSerializer,
                        QuoteManagerSerializer,
                        RequestSerializer,
                        TicketSerializer,
                        sendRequestSerializer)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from .models import Bet, Contest, QuoteManager, Request, Ticket

class GamesView(ViewSet):
    def list(self, request):
        queryset = Game.objects.all()
        serializer = GameSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Game.objects.all()
        game = get_object_or_404(queryset,pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)


class RequestView(ViewSet):
    def create(self, request):
        data = request.data
        print(request.user.id)
        data_serializable = {
            "user": request.user.id,
            "option": int(data['option']),
            "quotes": int(data['quotes']),
            "suggested_numbers": data['suggested_numbers']
        }
        serializer = sendRequestSerializer(data = data_serializable)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data, status=status.HTTP_201_CREATED)
    
    def list(self, request):
        req = Request.objects.filter(user = request.user)
        serializer = RequestSerializer(req, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk):
        try:
            req = Request.objects.filter(user=request.user).get(id=pk)
            serializer = RequestSerializer(req)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Request.DoesNotExist:
            return Response({'error':'request not found'},status=status.HTTP_404_NOT_FOUND)

class ContestView(ViewSet):
    def retrieve(self, request, pk):
        try:
            data = Contest.objects.get(pk=pk)
            serializer = ContestSerializer(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Contest.DoesNotExist:
            return Response({'error':'contest not found'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        data = Contest.objects.all()
        serializer = ContestSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
     
class BetView(ViewSet):
    def retrieve(self, request, pk):
        try:
            bet = Bet.objects.get(ticket__id=pk)
            serializer = BetSerializer(bet)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
    def list(self, request):
        requests = Request.objects.filter(user = request.user)
        bets = []
        for r in requests.all():
            try:
                qm = QuoteManager.objects.get(request=r)
                ticket = qm.ticket
            except QuoteManager.DoesNotExist:
                continue
            bets += Bet.objects.filter(ticket__id=ticket.id)
        serializer = BetSerializer(bets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TicketView(ViewSet):    
    def retrieve(self, request, pk):
        requests = Request.objects.filter(user = request.user)
        for r in requests.all():
            try:
                qm = QuoteManager.objects.get(request=r)
                ticket = qm.ticket
                if(ticket.id == pk):
                    serializer =  TicketSerializer(ticket)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                continue
        return Response({'error':'ticket not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        requests = Request.objects.filter(user = request.user)
        tickets = []
        for r in requests.all():
            try:
                qm = QuoteManager.objects.get(request=r)
                if(qm.ticket not in tickets):
                    tickets.append(qm.ticket)
            except:
                continue
        if(len(tickets) > 0):
            serializer =  TicketSerializer(tickets, many=True)
            return Response(
                    serializer.data, 
                    status=status.HTTP_200_OK)
        return Response(
                {'error':'ticket not found'}, 
                status=status.HTTP_404_NOT_FOUND)

class Cart(ViewSet):
    def list(self, request):
        user = request.user
        cart = Request.objects.filter(user=user, status='open')
        serializer = CartSerializer(cart, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        user = request.user
        try:
            betrequest = Request.objects.get(user=user, pk=pk)
            print(betrequest)
            betrequest.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def pay(self, request):
        user = request.user
        cart = Request.objects.filter(user=user, status='open')
        for req in cart:
            req.status = 'paid'
            req.save()
        if(len(cart) > 0):
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class CartLength(APIView):
    def get(self, request):
        user = request.user
        cartlist = Request.objects.filter(user=user, status='open')
        length = len(cartlist)
        return Response(length)

class QuoteManagerView(APIView):
    def get(self, request):
        user = request.user
        manager = QuoteManager.objects.filter(request__user=user)
        serializer = QuoteManagerSerializer(manager, many=True)
        if(len(serializer.data)>0):
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status.HTTP_404_NOT_FOUND)