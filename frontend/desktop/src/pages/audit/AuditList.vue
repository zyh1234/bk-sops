/**
* Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
* Edition) available.
* Copyright (C) 2017-2019 THL A29 Limited, a Tencent company. All rights reserved.
* Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
* http://opensource.org/licenses/MIT
* Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
* an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
* specific language governing permissions and limitations under the License.
*/
<template>
    <div class="audit-container">
        <div class="list-wrapper">
            <base-title :title="i18n.auditList"></base-title>
            <div class="operation-area clearfix">
                <advance-search-form
                    :search-config="{ placeholder: i18n.taskNamePlaceholder }"
                    :search-form="searchForm"
                    @onSearchInput="onSearchInput"
                    @submit="onSearchFormSubmit">
                </advance-search-form>
            </div>
            <div class="audit-table-content">
                <bk-table
                    :data="auditList"
                    :pagination="pagination"
                    v-bkloading="{ isLoading: listLoading, opacity: 1 }"
                    @page-change="onPageChange">
                    <bk-table-column label="ID" prop="id" width="80"></bk-table-column>
                    <bk-table-column :label="i18n.business" prop="project.name" width="120"></bk-table-column>
                    <bk-table-column :label="i18n.name">
                        <template slot-scope="props">
                            <a
                                v-if="!hasPermission(['view'], props.row.auth_actions, taskOperations)"
                                v-cursor
                                class="text-permission-disable"
                                :title="props.row.name"
                                @click="onTemplatePermissonCheck(props.row)">
                                {{props.row.name}}
                            </a>
                            <router-link
                                v-else
                                class="task-name"
                                :title="props.row.name"
                                :to="{
                                    name: 'auditTaskExecute',
                                    params: { project_id: props.row.project.id },
                                    query: { instance_id: props.row.id }
                                }">
                                {{props.row.name}}
                            </router-link>
                        </template>
                    </bk-table-column>
                    <bk-table-column :label="i18n.startedTime" width="200">
                        <template slot-scope="props">
                            {{ props.row.start_time || '--' }}
                        </template>
                    </bk-table-column>
                    <bk-table-column :label="i18n.finishedTime" width="200">
                        <template slot-scope="props">
                            {{ props.row.finish_time || '--' }}
                        </template>
                    </bk-table-column>
                    <bk-table-column :label="i18n.category" prop="category_name" width="100"></bk-table-column>
                    <bk-table-column :label="i18n.creator" prop="creator_name" width="100"></bk-table-column>
                    <bk-table-column :label="i18n.operator" width="100">
                        <template slot-scope="props">
                            {{ props.row.executor_name || '--' }}
                        </template>
                    </bk-table-column>
                    <bk-table-column :label="i18n.status" width="120">
                        <template slot-scope="props">
                            <div class="audit-status">
                                <span :class="executeStatus[props.$index] && executeStatus[props.$index].cls"></span>
                                <span class="task-status-text" v-if="executeStatus[props.$index]">{{executeStatus[props.$index].text}}</span>
                            </div>
                        </template>
                    </bk-table-column>
                    <bk-table-column :label="i18n.operation" width="100">
                        <template slot-scope="props">
                            <a
                                v-if="!hasPermission(['view'], props.row.auth_actions, taskOperations)"
                                v-cursor
                                class="text-permission-disable"
                                @click="onTemplatePermissonCheck(props.row)">
                                {{i18n.view}}
                            </a>
                            <router-link
                                v-else
                                class="audit-operation-btn"
                                :to="{
                                    name: 'auditTaskExecute',
                                    params: { project_id: props.row.project.id },
                                    query: { instance_id: props.row.id }
                                }">
                                {{ i18n.view }}
                            </router-link>
                        </template>
                    </bk-table-column>
                    <div class="empty-data" slot="empty"><NoData /></div>
                </bk-table>
            </div>
        </div>
        <CopyrightFooter></CopyrightFooter>
    </div>
</template>
<script>
    import '@/utils/i18n.js'
    import { mapState, mapActions } from 'vuex'
    import { errorHandler } from '@/utils/errorHandler.js'
    import permission from '@/mixins/permission.js'
    import CopyrightFooter from '@/components/layout/CopyrightFooter.vue'
    import NoData from '@/components/common/base/NoData.vue'
    import BaseTitle from '@/components/common/base/BaseTitle.vue'
    import AdvanceSearchForm from '@/components/common/advanceSearchForm/index.vue'
    import toolsUtils from '@/utils/tools.js'
    import moment from 'moment-timezone'
    import task from '@/mixins/task.js'
    const searchForm = [
        {
            type: 'select',
            label: gettext('所属项目'),
            key: 'selectedProject',
            loading: false,
            placeholder: gettext('请选择所属项目'),
            list: []
        },
        {
            type: 'dateRange',
            key: 'executeTime',
            placeholder: gettext('选择日期时间范围'),
            label: gettext('执行开始'),
            value: []
        },
        {
            type: 'select',
            label: gettext('任务分类'),
            key: 'category',
            loading: false,
            placeholder: gettext('请选择分类'),
            list: []
        },
        {
            type: 'input',
            key: 'creator',
            label: gettext('创建人'),
            placeholder: gettext('请输入创建人'),
            value: ''
        },
        {
            type: 'input',
            key: 'executor',
            label: gettext('执行人'),
            placeholder: gettext('请输入执行人'),
            value: ''
        },
        {
            type: 'select',
            label: gettext('状态'),
            key: 'statusSync',
            loading: false,
            placeholder: gettext('请选择状态'),
            list: [
                { 'value': 'nonExecution', 'name': gettext('未执行') },
                { 'value': 'runing', 'name': gettext('未完成') },
                { 'value': 'finished', 'name': gettext('完成') }
            ]
        }
    ]
    export default {
        name: 'auditHome',
        components: {
            AdvanceSearchForm,
            CopyrightFooter,
            BaseTitle,
            NoData
        },
        mixins: [permission, task],
        data () {
            return {
                i18n: {
                    auditList: gettext('审计中心'),
                    placeholder: gettext('请输入ID或流程名称'),
                    business: gettext('所属项目'),
                    startedTime: gettext('执行开始'),
                    finishedTime: gettext('执行结束'),
                    name: gettext('任务名称'),
                    category: gettext('任务类型'),
                    creator: gettext('创建人'),
                    operator: gettext('执行人'),
                    status: gettext('状态'),
                    operation: gettext('操作'),
                    view: gettext('查看'),
                    total: gettext('共'),
                    item: gettext('条记录'),
                    comma: gettext('，'),
                    currentPageTip: gettext('当前第'),
                    page: gettext('页'),
                    executing: gettext('执行中'),
                    pauseState: gettext('暂停'),
                    taskType: gettext('任务分类'),
                    query: gettext('搜索'),
                    reset: gettext('清空'),
                    dateRange: gettext('选择日期时间范围')
                },
                taskBasicInfoLoading: true,
                listLoading: true,
                activeTaskCategory: undefined,
                business: {
                    list: [],
                    loading: false,
                    id: null,
                    searchable: true,
                    empty: false
                },
                auditList: [],
                taskCategory: [],
                executeStatus: [], // 任务执行态
                requestData: {
                    selectedProject: '',
                    executeTime: [],
                    category: '',
                    creator: '',
                    executor: '',
                    statusSync: '',
                    flowName: ''
                },
                pagination: {
                    current: 1,
                    count: 0,
                    limit: 15,
                    'limit-list': [15],
                    'show-limit': false
                },
                taskOperations: [],
                taskResource: {}
            }
        },
        computed: {
            ...mapState('project', {
                'timeZone': state => state.timezone
            }),
            searchForm () {
                const value = searchForm
                value[0].list = this.business.list.map(m => ({ name: m.name, value: m.id }))
                value[2].list = this.taskCategory
                return searchForm
            }
        },
        created () {
            this.loadAuditTask()
            this.onSearchInput = toolsUtils.debounce(this.searchInputhandler, 500)
            this.getProjectList()
            this.getProjectBaseInfo()
        },
        methods: {
            ...mapActions('auditTask/', [
                'loadAuditTaskList'
            ]),
            ...mapActions('task/', [
                'getInstanceStatus'
            ]),
            ...mapActions('template/', [
                'loadProjectBaseInfo'
            ]),
            ...mapActions('project/', [
                'loadProjectList'
            ]),
            async loadAuditTask () {
                this.listLoading = true
                try {
                    const { selectedProject, executeTime, category, creator, executor, statusSync, flowName } = this.requestData
                    let pipeline_instance__is_started
                    let pipeline_instance__is_finished
                    if (statusSync) {
                        pipeline_instance__is_started = statusSync !== 'nonExecution'
                        pipeline_instance__is_finished = statusSync === 'finished'
                    }
                    const data = {
                        limit: this.pagination.limit,
                        offset: (this.pagination.current - 1) * this.pagination.limit,
                        project__id: selectedProject || undefined,
                        category: category || undefined,
                        audit__pipeline_instance__name__contains: flowName || undefined,
                        pipeline_instance__is_started,
                        pipeline_instance__is_finished,
                        pipeline_instance__creator__contains: creator || undefined,
                        pipeline_instance__executor__contains: executor || undefined
                    }
                    if (executeTime[0] && executeTime[1]) {
                        if (this.common) {
                            data['pipeline_template__start_time__gte'] = moment(executeTime[0]).format('YYYY-MM-DD')
                            data['pipeline_template__start_time__lte'] = moment(executeTime[1]).add('1', 'd').format('YYYY-MM-DD')
                        } else {
                            data['pipeline_instance__start_time__gte'] = moment.tz(executeTime[0], this.timeZone).format('YYYY-MM-DD')
                            data['pipeline_instance__start_time__lte'] = moment.tz(executeTime[1], this.timeZone).add('1', 'd').format('YYYY-MM-DD')
                        }
                    }
                    const auditListData = await this.loadAuditTaskList(data)
                    const list = auditListData.objects
                    this.auditList = list
                    this.pagination.count = auditListData.meta.total_count
                    this.taskOperations = auditListData.meta.auth_operations
                    this.taskResource = auditListData.meta.auth_resource
                    this.totalCount = auditListData.meta.total_count
                    // mixins getExecuteStatus
                    this.getExecuteStatus('executeStatus', list)
                } catch (e) {
                    errorHandler(e, this)
                } finally {
                    this.listLoading = false
                }
            },
            onPageChange (page) {
                this.pagination.current = page
                this.loadAuditTask()
            },
            searchInputhandler (data) {
                this.requestData.flowName = data
                this.pagination.current = 1
                this.loadAuditTask()
            },
            async getProjectList () {
                this.business.loading = true
                try {
                    const businessData = await this.loadProjectList({ limit: 0 })
                    this.business.list = businessData.objects
                } catch (e) {
                    errorHandler(e, this)
                } finally {
                    this.business.loading = false
                }
            },
            async getProjectBaseInfo () {
                this.taskBasicInfoLoading = true
                try {
                    const data = await this.loadProjectBaseInfo()
                    this.taskCategory = data.task_categories.map(m => ({ name: m.name, value: m.value }))
                } catch (e) {
                    errorHandler(e, this)
                } finally {
                    this.taskBasicInfoLoading = false
                }
            },
            onClearCategory () {
                this.activeTaskCategory = undefined
            },
            onSelectedCategory (id) {
                this.activeTaskCategory = id
            },
            onTemplatePermissonCheck (task) {
                if (!this.hasPermission(['view'], task.auth_actions, this.taskOperations)) {
                    this.applyForPermission(['view'], task, this.taskOperations, this.taskResource)
                }
            },
            onSearchFormSubmit (data) {
                this.requestData = data
                this.loadAuditTask()
            }
        }
    }
</script>
<style lang='scss' scoped>
@import '@/scss/config.scss';
@import '@/scss/task.scss';
.bk-select-inline,.bk-input-inline {
    display: inline-block;
    width: 260px;
}
.audit-container {
    min-width: 1320px;
    min-height: calc(100% - 50px);
    background: #fafafa;
}
.list-wrapper {
    padding: 0 60px;
    min-height: calc(100vh - 240px);
    .advanced-search {
        margin: 0;
    }
}
.operation-area {
    margin: 20px 0;
    .common-icon-search {
        position: absolute;
        right: 15px;
        top: 8px;
        color: $commonBorderColor;
    }
}
.common-icon-dark-circle-pause {
    color: #ff9C01;
    font-size: 12px;
}
.audit-table-content {
    background: #ffffff;
    a.task-name {
        color: $blueDefault;
    }
    .audit-status {
        @include ui-task-status;
    }
    .audit-operation-btn {
        color: #3c96ff;
    }
    .empty-data {
        padding: 120px 0;
    }
}
.panagation {
    padding: 10px 20px;
    text-align: right;
    border: 1px solid #dde4eb;
    border-top: none;
    background: #fafbfd;
    .page-info {
        float: left;
        line-height: 36px;
        font-size: 14px;
    }
    .bk-page {
        display: inline-block;
    }
}
</style>