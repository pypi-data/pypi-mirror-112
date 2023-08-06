import trafaret as t

from datarobot import Model
from datarobot._experimental.models.segment import SegmentInfo


class CombinedModel(Model):
    """
    A model from a segmented project. Combination of ordinary models in child segments projects.

    Attributes
    ----------
    id : str
        the id of the model
    project_id : str
        the id of the project the model belongs to
    segmentation_task_id : str
        the id of a segmentation task used in this model
    """

    _converter = t.Dict(
        {
            t.Key("combined_model_id") >> "id": t.String,
            t.Key("project_id"): t.String,
            t.Key("segmentation_task_id"): t.String,
        }
    ).ignore_extra("*")

    def __init__(self, id=None, project_id=None, segmentation_task_id=None):
        self.id = id
        self.project_id = project_id
        self.segmentation_task_id = segmentation_task_id

    def __repr__(self):
        return "CombinedModel({})".format(self.id)

    @classmethod
    def get(cls, project_id, combined_model_id):
        """ Retrieve combined model

        Parameters
        ----------
        project_id : str
            The project's id.
        combined_model_id : str
            Id of the combined model.

        Returns
        -------
        CombinedModel
            The queried combined model.
        """
        url = "projects/{}/combinedModels/{}/".format(project_id, combined_model_id)
        return cls.from_location(url)

    def get_segments_info(self):
        """Retrieve Combined Model segments info

        Returns
        -------
        list[SegmentInfo]
            List of segments
        """
        return SegmentInfo.list(self.project_id, self.id)
