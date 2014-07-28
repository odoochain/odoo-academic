# -*- coding: utf-8 -*-
from openerp import tools
from openerp import models, fields, api, _

class academic_evaluation_analysis(models.Model):
    _name = "academic.evaluation.analysis"
    _description = "Academic Evaluation Analysis"
    _auto = False

    # Survey Fields
    is_evaluation = fields.Boolean('Is Evaluation?', readonly=True,)
    survey_id = fields.Many2one('survey.survey', 'Survey', readonly=True,)
    survey_stage_id = fields.Many2one('survey.stage', string="Stage", readonly=True,)
    period_id =  fields.Many2one('academic.period', string='Period', readonly=True,)
    
    # Group evaluation
    group_evaluation_state = fields.Selection([(u'invisible', u'Invisible'), (u'visible', u'Visible'), (u'open', u'Open'), (u'closed', u'Closed')], 'Group Ev. Status', readonly=True)

    # User Input
    input_state = fields.Selection([('done', 'Finished '),('skip', 'Not Finished')], 'Status', readonly=True)
    group_id = fields.Many2one('academic.group', 'Group', readonly=True,)
    partner_id = fields.Many2one('res.partner', 'Partner', readonly=True,)
    company_id = fields.Many2one('res.company', 'Company', readonly=True,)
    avg_score = fields.Float('Avg Score', readonly=True, group_operator='avg',)
    min_score = fields.Float('Min Score', readonly=True, group_operator='min',)
    max_score = fields.Float('Max Score', readonly=True, group_operator='max',)

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'academic_evaluation_analysis')
        cr.execute("""
            create or replace view academic_evaluation_analysis as (
SELECT
        survey_user_input.id as id,
        survey_user_input.score as avg_score,
        survey_user_input.score as min_score,
        survey_user_input.score as max_score,
        survey_user_input.survey_id as survey_id,
        survey_user_input.partner_id as partner_id,
        survey_user_input.state as input_state,
        academic_group_evaluation.group_id as group_id,
        academic_group_evaluation.state as group_evaluation_state,
        academic_group.company_id,
        survey_survey.is_evaluation as is_evaluation,
        survey_survey.stage_id as survey_stage_id,
        survey_survey.period_id as period_id        
    FROM survey_user_input
    INNER JOIN survey_survey
    on survey_user_input.survey_id = survey_survey.id
    FULL JOIN academic_group_evaluation
        on survey_user_input.group_evaluation_id = academic_group_evaluation.id  
    FULL JOIN academic_group
        on academic_group_evaluation.group_id = academic_group.id  
        )
        """)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
