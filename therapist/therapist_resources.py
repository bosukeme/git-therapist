from flask_restful import Resource, reqparse
from therapist.get_therapist import get_details_of_therapist


class TherapistDiscovery(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('profile_url', type=str, help="The profile url of the therapist")
            args = parser.parse_args()


            result = get_details_of_therapist(args['profile_url'])
            return {
                'status': 'success',
                'data': result, 
                'message': 'Therapist details successful.'
            }, 200

        except Exception as e:
            return {
                'status': 'failed',
                'data': None,
                'message': str(e)
            }, 500
