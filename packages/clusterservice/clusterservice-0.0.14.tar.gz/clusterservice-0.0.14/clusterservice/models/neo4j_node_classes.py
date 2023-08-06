from neomodel import (
    FloatProperty,
    IntegerProperty,
    Relationship,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    StructuredRel,
    UniqueIdProperty,
    DateTimeProperty,
    BooleanProperty,
)


class Client(StructuredNode):
    client_id = StringProperty(required=True, unique_index = True)
    client_taxonomy_config = StringProperty(required=True)


class ProblemSolution(StructuredNode):
    argument_type = StringProperty(required=True)  # Problem or Solution
    pro_con_flag = StringProperty(required=True)  # Pro or Con
    process_datetime = DateTimeProperty(default_now=True)


class Topic(StructuredNode):
    text = StringProperty(required=True, unique_index = True)
    tsne_coords = StringProperty(required=True)
    process_datetime = DateTimeProperty(default_now=True)

class TopicRel(StructuredRel):
    confidence = FloatProperty(required=False, default=1)


class SubTopic(StructuredNode):
    text = StringProperty(required=True, unique_index = True)
    topic = Relationship(Topic, 'HAS_TOPIC', model=TopicRel)
    process_datetime = DateTimeProperty(default_now=True)

class SubTopicRel(StructuredRel):
    confidence = FloatProperty(required=False)


class Sentiment(StructuredNode):
    sentiment = IntegerProperty(required=True, unique_index=True)
    process_datetime = DateTimeProperty(default_now=True)


class UserMood(StructuredNode):
    mood = IntegerProperty(required=True, unique_index=True)

    
class Emoji(StructuredNode):
    label = StringProperty(required=True)
    pax_label = StringProperty(required=True)
    group = StringProperty(required=True)
    plutchik_category = StringProperty()
    process_datetime = DateTimeProperty(default_now=True)


class EmojiRel(StructuredRel):
    intensity = IntegerProperty(required=False)
    probability = FloatProperty(required=False)


class EntityType(StructuredNode):
    text = StringProperty(required=True, unique_index = True)
    process_datetime = DateTimeProperty(default_now=True)


class Entity(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    type = Relationship(EntityType, 'OF_TYPE')
    process_datetime = DateTimeProperty(default_now=True)
    

class EntityTypeRel(StructuredRel):
    confidence = FloatProperty(required=False)


class UserDemographics(StructuredNode):
    client_id = StringProperty(required=True)
    taxonomy = StringProperty(required=True)
    value = StringProperty(required=True)
    category = StringProperty()

# With inherited classes neomodel creates multiple labels to the node 
# (i.e. the class name and each inherited class name will be a label associated to the node)
class CustomDemographic(UserDemographics):
    parent = Relationship('CustomDemographic', 'HAS_PARENT_PROPERTY')


class AgeGroup(UserDemographics):
    pass


class GenderIdentity(UserDemographics):
    pass


class Location(UserDemographics):
    category = StringProperty(default='GeoLocation')


class Ethnicity(UserDemographics):
    pass


class EducationLevel(UserDemographics):
    pass


class Occupation(UserDemographics):
    pass


class User(StructuredNode):
    uid = StringProperty(required=True, unique_index = True)
    client_id = StringProperty(required=True)
    anonymous = BooleanProperty()
    process_datetime = DateTimeProperty(default_now=True)
    age_group = Relationship(AgeGroup, 'HAS_DEMOGRAPHIC')
    ethnicity = Relationship(Ethnicity, 'HAS_DEMOGRAPHIC')
    location = Relationship(Location, 'HAS_DEMOGRAPHIC')
    gender_identity = Relationship(GenderIdentity, 'HAS_DEMOGRAPHIC')
    custom_demographic = Relationship(CustomDemographic, 'HAS_DEMOGRAPHIC')
    #TODO need to check if there is a cleaner way
    #class_relation_map is added to be able to dynamically associate the class object name with the reltionship attribute object name in User node
    #used in write_user_demographics
    class_relation_map = {'CustomDemographic':'custom_demographic',
                'AgeGroup':'age_group',
                'GenderIdentity':'gender_identity',
                'Location':'location',
                'Ethnicity':'ethnicity',
            }
    
class Comment(StructuredNode):
    uid = StringProperty(required=True, unique_index = True)
    text = StringProperty(required=True)
    client_id = StringProperty(required=True)
    forum_id = StringProperty(required=True)
    conversation_id = StringProperty()
    create_datetime = DateTimeProperty(default_now=False)
    process_datetime = DateTimeProperty(default_now=True)
    number_likes = IntegerProperty(default=0)
    number_dislikes = IntegerProperty(default=0)
    number_good_rating = IntegerProperty(default=0)
    number_replies = IntegerProperty(default=0)
    avg_sentiment = Relationship(Sentiment, 'HAS_AVG_SENTIMENT')
    emoji = Relationship(Emoji, 'HAS_EMOJI', model=EmojiRel)
    topic = Relationship(Topic, 'HAS_TOPIC', model=TopicRel)
    subtopic = Relationship(SubTopic, 'HAS_SUBTOPIC', model=SubTopicRel)
    user = Relationship(User, 'POSTED_BY')
    entity = Relationship(Entity, 'HAS_ENTITY')
    user_mood = Relationship(UserMood, 'HAS_USER_MOOD')

class Sentence(StructuredNode):
    uid = UniqueIdProperty()
    text = StringProperty(required=True)
    client_id = StringProperty(required=True)
    forum_id = StringProperty(required=True)
    conversation_id = StringProperty()
    process_datetime = DateTimeProperty(default_now=True)
    comment = Relationship(Comment, 'DECOMPOSES')
    sentiment = Relationship(Sentiment, 'HAS_SENTIMENT')
    emoji = Relationship(Emoji, 'HAS_EMOJI', model=EmojiRel)
    topic = Relationship(Topic, 'HAS_TOPIC', model=TopicRel)
    subtopic = Relationship(SubTopic, 'HAS_SUBTOPIC', model=SubTopicRel)


class Chunk(StructuredNode):
    uid = UniqueIdProperty()
    text = StringProperty(required=True)
    client_id = StringProperty(required=True)
    forum_id = StringProperty(required=True)
    conversation_id = StringProperty()
    process_datetime = DateTimeProperty(default_now=True)
    comment = Relationship(Comment, 'DECOMPOSES')
    sentiment = Relationship(Sentiment, 'HAS_SENTIMENT')
    emoji = Relationship(Emoji, 'HAS_EMOJI', model=EmojiRel)
    topic = Relationship(Topic, 'HAS_TOPIC', model=TopicRel)
    subtopic = Relationship(SubTopic, 'HAS_SUBTOPIC', model=SubTopicRel)
    entity = Relationship(Entity, 'HAS_ENTITY')
    argument = Relationship(ProblemSolution, 'HAS_ARGUMENT')


class Question(StructuredNode):
    uid = UniqueIdProperty()
    text = StringProperty(required=True)
    client_id = StringProperty(required=True)
    forum_id = StringProperty(required=True)
    conversation_id = StringProperty()
    process_datetime = DateTimeProperty(default_now=True)


class ClusterHead(StructuredNode):
    uid = UniqueIdProperty()
    text = StringProperty(required=True)
    similarity_score = FloatProperty(required=True)
    element_count = IntegerProperty()
    client_id = StringProperty(required=True)
    forum_id = StringProperty(required=True)
    conversation_id = StringProperty()
    process_datetime = DateTimeProperty(default_now=True)
    question = Relationship(Question, 'ANSWERS')


class ClusterElement(StructuredNode):
    uid = UniqueIdProperty()
    text = StringProperty(required=True)
    client_id = StringProperty(required=True)
    forum_id = StringProperty(required=True)
    conversation_id = StringProperty()
    process_datetime = DateTimeProperty(default_now=True)
    sentences = Relationship(Sentence, 'DERIVES_FROM')
    chunks = Relationship(Chunk, 'DERIVES_FROM')
    cluster_head = Relationship(ClusterHead, 'DECOMPOSES')

