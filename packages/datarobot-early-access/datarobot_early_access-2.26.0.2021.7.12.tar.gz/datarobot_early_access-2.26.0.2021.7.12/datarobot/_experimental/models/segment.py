import trafaret as t

from datarobot.models.api_object import APIObject
from datarobot.utils import encode_utf8_if_py2
from datarobot.utils.pagination import unpaginate


class Segment(APIObject):
    """
    A Segment is a child project of existing segmented project.

    Attributes
    ----------
    project_id : ObjectId
        The associated id of the child project.
    segment : str
        the name of the segment
    """

    _base_url = "projects/{}/segments/"

    _converter = t.Dict(
        {t.Key("project_id", optional=True): t.String | t.Null, t.Key("segment"): t.String}
    ).ignore_extra("*")

    def __init__(self, project_id=None, segment=None):
        self.project_id = project_id
        self.segment = segment

    def __repr__(self):
        return encode_utf8_if_py2(
            u"Segment(segment={}, project_id={})".format(self.segment, self.project_id)
        )

    @classmethod
    def list(cls, project_id):
        """
        List all of the segments that have been created for a specific project_id.

        Parameters
        ----------
        project_id : basestring
            The id of the parent project

        Returns
        -------
        segments : list of Segment
            List of instances with initialized data.
        """

        return [
            cls.from_server_data(x)
            for x in unpaginate(
                initial_url=cls._base_url.format(project_id),
                initial_params=None,
                client=cls._client,
            )
        ]


class SegmentInfo(APIObject):
    """
    A SegmentInfo is an object containing information about the combined model segments

    Attributes
    ----------
    project_id : ObjectId
        The associated id of the child project.
    segment : str
        the name of the segment
    project_stage : str
        A description of the current stage of the project
    project_status_error : str
        Project status error message.
    autopilot_done : str
        Is autopilot done for the project.
    model_count : int
        Count of trained models in project.
    model_id : str
        ID of segment champion model.
    """

    _base_url = "projects/{}/combinedModels/{}/segments/"

    _converter = t.Dict(
        {
            t.Key("project_id"): t.String,
            t.Key("segment"): t.String,
            t.Key("project_stage"): t.String,
            t.Key("project_status_error"): t.String(allow_blank=True),
            t.Key("autopilot_done"): t.Bool,
            t.Key("model_count", optional=True): t.Int | t.Null,
            t.Key("model_id", optional=True): t.String | t.Null,
        }
    ).ignore_extra("*")

    def __init__(
        self,
        project_id=None,
        segment=None,
        project_stage=None,
        project_status_error=None,
        autopilot_done=None,
        model_count=None,
        model_id=None,
    ):
        self.project_id = project_id
        self.segment = segment
        self.project_stage = project_stage
        self.project_status_error = project_status_error
        self.autopilot_done = autopilot_done
        self.model_count = model_count
        self.model_id = model_id

    def __repr__(self):
        return encode_utf8_if_py2(
            u"SegmentInfo(segment={}, project_id={}, autopilot_done={})".format(
                self.segment, self.project_id, self.autopilot_done
            )
        )

    @classmethod
    def list(cls, project_id, model_id):
        """
        List all of the segments that have been created for a specific project_id.

        Parameters
        ----------
        project_id : basestring
            The id of the parent project

        Returns
        -------
        segments : list of Segment
            List of instances with initialized data.
        """

        return [
            cls.from_server_data(x)
            for x in unpaginate(
                initial_url=cls._base_url.format(project_id, model_id),
                initial_params=None,
                client=cls._client,
            )
        ]
