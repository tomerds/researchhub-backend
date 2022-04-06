import datetime
import pytz
from time import time

class Distribution:
    def __init__(self, name, amount, give_rep=True):
        self._name = name
        self._amount = amount
        self._give_rep = give_rep

    @property
    def name(self):
        return self._name

    @property
    def amount(self):
        return self._amount

    @property
    def gives_rep(self):
        return self._give_rep

RSC_YEARLY_GIVEAWAY = 50000000
MINUTES_IN_YEAR = 525960
HOURS_IN_YEAR = MINUTES_IN_YEAR / 60
DAYS_IN_YEAR = 365
MONTHS_IN_YEAR = 12
GROWTH = .2

def calculate_upvote_rsc():
    from paper.models import Vote
    from discussion.models import (
        Vote as ReactionVote
    )

    def calculate_rsc(timeframe, weight):
        return RSC_YEARLY_GIVEAWAY * weight / timeframe

    def calculate_votes(timeframe):
        return Vote.objects.filter(vote_type=1, created_date__gte=timeframe).count() + ReactionVote.objects.filter(vote_type=1, created_date__gte=timeframe).count()

    today = datetime.datetime.now(
        tz=pytz.utc
    ).replace(
        hour=0,
        minute=0,
        second=0
    )
    past_minute = today - datetime.timedelta(minutes=1)
    past_hour = today - datetime.timedelta(minutes=60)
    past_day = today - datetime.timedelta(days=1)
    past_month = today - datetime.timedelta(days=30)
    past_year = today - datetime.timedelta(days=365)

    votes_in_past_minute = calculate_votes(past_minute)
    votes_in_past_hour = calculate_votes(past_hour)
    votes_in_past_day = calculate_votes(past_day)
    votes_in_past_month = calculate_votes(past_month)
    votes_in_past_year = calculate_votes(past_year)

    rsc_by_minute = calculate_rsc(votes_in_past_minute * MINUTES_IN_YEAR, .25)
    rsc_by_hour = calculate_rsc(votes_in_past_hour * HOURS_IN_YEAR, .3)
    rsc_by_day = calculate_rsc(votes_in_past_day * DAYS_IN_YEAR, .25)
    rsc_by_month = calculate_rsc(votes_in_past_month * MONTHS_IN_YEAR, .1)
    rsc_by_year = calculate_rsc(votes_in_past_year, .1)

    rsc_distribute = rsc_by_minute + rsc_by_hour + rsc_by_day + rsc_by_month + rsc_by_year
    rsc_distribute *= (1 - GROWTH)

    return int(rsc_distribute)

def create_upvote_distribution(vote_type, paper):
    distribution_amount = calculate_upvote_rsc()

    if paper:
        from reputation.distributor import Distributor
        author_distribution_amount = distribution_amount * .75
        distribution_amount *= .25 # authors get 75% of the upvote score
        distributed_amount = 0
        author_count = paper.true_author_count()

        for author in paper.authors.all():
            if author.user:
                timestamp = time()
                amt = author_distribution_amount / author_count
                distributor = Distributor(
                    Distribution(vote_type, amt),
                    author.user,
                    paper,
                    timestamp,
                    paper.hubs.all(),
                )
                record = distributor.distribute()
                distributed_amount += amt
        

        from reputation.models import AuthorRSC
        AuthorRSC.objects.create(
            paper=paper,
            amount=author_distribution_amount - distributed_amount,
        )

    return Distribution(
        vote_type, distribution_amount
    )

FlagPaper = Distribution(
    'FLAG_PAPER', 1
)
PaperUpvoted = Distribution(
    'PAPER_UPVOTED', 1
)

CreateBulletPoint = Distribution(
    'CREATE_BULLET_POINT', 1
)
BulletPointCensored = Distribution(
    'BULLET_POINT_CENSORED', -2
)
BulletPointFlagged = Distribution(
    'BULLET_POINT_FLAGGED', -2
)
BulletPointUpvoted = Distribution(
    'BULLET_POINT_UPVOTED', 1
)
BulletPointDownvoted = Distribution(
    'BULLET_POINT_DOWNVOTED', -1
)

CommentCensored = Distribution(
    'COMMENT_CENSORED', -2
)
CommentFlagged = Distribution(
    'COMMENT_FLAGGED', -2
)
CommentUpvoted = Distribution(
    'COMMENT_UPVOTED', 1
)
CommentDownvoted = Distribution(
    'COMMENT_DOWNVOTED', -1
)

ReplyCensored = Distribution(
    'REPLY_CENSORED', -2
)
ReplyFlagged = Distribution(
    'REPLY_FLAGGED', -2
)
ReplyUpvoted = Distribution(
    'REPLY_UPVOTED', 1
)
ReplyDownvoted = Distribution(
    'REPLY_DOWNVOTED', -1
)

ThreadCensored = Distribution(
    'THREAD_CENSORED', -2
)
ThreadFlagged = Distribution(
    'THREAD_FLAGGED', -2
)
ThreadUpvoted = Distribution(
    'THREAD_UPVOTED', 1
)
ThreadDownvoted = Distribution(
    'THREAD_DOWNVOTED', -1
)

CreateSummary = Distribution(
    'CREATE_SUMMARY', 1
)
CreateFirstSummary = Distribution(
    'CREATE_FIRST_SUMMARY', 5
)
SummaryApproved = Distribution(
    'SUMMARY_APPROVED', 15
)
SummaryRejected = Distribution(
    'SUMMARY_REJECTED', -2
)
SummaryFlagged = Distribution(
    'SUMMARY_FLAGGED', -5
)
SummaryUpvoted = Distribution(
    'SUMMARY_UPVOTED', 1
)
SummaryDownvoted = Distribution(
    'SUMMARY_DOWNVOTED', -1
)
ResearchhubPostUpvoted = Distribution(
    'RESEARCHHUB_POST_UPVOTED', 1
)
ResearchhubPostDownvoted = Distribution(
    'RESEARCHHUB_POST_DOWNVOTED', -1
)
ResearchhubPostCensored = Distribution(
    'RESEARCHHUB_POST_CENSORED', -2
)
Referral = Distribution(
    'REFERRAL', 50, False
)

ReferralApproved = Distribution(
    'REFERRAL_APPROVED', 1000, False
)

NeutralVote = Distribution('NEUTRAL_VOTE', 0)


def create_purchase_distribution(amount):
    return Distribution(
        'PURCHASE', amount
    )


DISTRIBUTION_TYPE_CHOICES = [
    (
        FlagPaper.name,
        FlagPaper.name
    ),
    (
        PaperUpvoted.name,
        PaperUpvoted.name
    ),
    (
        CreateBulletPoint.name,
        CreateBulletPoint.name
    ),
    (
        BulletPointFlagged.name,
        BulletPointFlagged.name
    ),
    (
        BulletPointUpvoted.name,
        BulletPointUpvoted.name
    ),
    (
        BulletPointDownvoted.name,
        BulletPointDownvoted.name
    ),
    (
        CommentCensored.name,
        CommentCensored.name
    ),
    (
        CommentFlagged.name,
        CommentFlagged.name
    ),
    (
        CommentUpvoted.name,
        CommentUpvoted.name
    ),
    (
        CommentDownvoted.name,
        CommentDownvoted.name
    ),
    (
        ReplyCensored.name,
        ReplyCensored.name
    ),
    (
        ReplyFlagged.name,
        ReplyFlagged.name
    ),
    (
        ReplyUpvoted.name,
        ReplyUpvoted.name
    ),
    (
        ReplyDownvoted.name,
        ReplyDownvoted.name
    ),
    (
        ThreadCensored.name,
        ThreadCensored.name
    ),
    (
        ThreadFlagged.name,
        ThreadFlagged.name
    ),
    (
        ThreadUpvoted.name,
        ThreadUpvoted.name
    ),
    (
        ThreadDownvoted.name,
        ThreadDownvoted.name
    ),
    (
        CreateSummary.name,
        CreateSummary.name
    ),
    (
        SummaryUpvoted.name,
        SummaryUpvoted.name
    ),
    (
        SummaryDownvoted.name,
        SummaryDownvoted.name
    ),
    (
        'UPVOTE_RSC_POT',
        'UPVOTE_RSC_POT'
    ),
    (
        'REWARD',
        'REWARD'
    ),
    (
        'PURCHASE',
        'PURCHASE'
    ),
    (
        Referral.name,
        Referral.name
    ),
    (
        'EDITOR_COMPENSATION',
        'EDITOR_COMPENSATION',
    )
]
