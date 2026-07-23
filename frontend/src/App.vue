<template>
  <div id="app">
    <el-container style="height:100vh;">
      <!-- 顶部导航 -->
      <el-header style="background:#409EFF;color:white;display:flex;align-items:center;padding:0 20px;">
        <span style="font-size:22px;font-weight:bold;">📚 图书管理系统</span>
        <span style="margin-left:20px;font-size:14px;opacity:0.8;">Flask + Vue 课设项目</span>
      </el-header>

      <el-container>
        <!-- 侧边栏 -->
        <el-aside width="200px" style="background:#2c3e50;color:white;padding-top:20px;">
          <el-menu
              background-color="#2c3e50"
              text-color="#fff"
              active-text-color="#409EFF"
              :default-active="currentMenu"
              @select="handleMenuSelect"
          >
            <el-menu-item index="books">
              <i class="el-icon-s-grid"></i>
              <span>图书管理</span>
            </el-menu-item>
            <el-menu-item index="borrow">
              <i class="el-icon-s-claim"></i>
              <span>借阅管理</span>
            </el-menu-item>
          </el-menu>
        </el-aside>

        <!-- 主内容区 -->
        <el-main style="background:#f0f2f5;">
          <!-- 图书管理页面 -->
          <div v-if="currentMenu === 'books'">
            <el-card shadow="never">
              <div style="display:flex;justify-content:space-between;margin-bottom:15px;">
                <div>
                  <el-input
                      placeholder="搜索书名或作者"
                      v-model="keyword"
                      style="width:220px;"
                      @keyup.enter="loadBooks"
                  >
                    <el-button slot="append" icon="el-icon-search" @click="loadBooks"></el-button>
                  </el-input>
                  <el-button type="primary" style="margin-left:10px;" @click="openAddDialog">+ 添加图书</el-button>
                </div>
                <span style="color:#909399;font-size:14px;">共 {{ books.length }} 本</span>
              </div>

              <el-table :data="books" border stripe style="width:100%;">
                <el-table-column prop="id" label="ID" width="60"></el-table-column>
                <el-table-column prop="bookName" label="书名" min-width="150"></el-table-column>
                <el-table-column prop="author" label="作者" width="120"></el-table-column>
                <el-table-column prop="isbn" label="ISBN" width="150"></el-table-column>
                <el-table-column label="状态" width="100">
                  <template slot-scope="scope">
                    <el-tag :type="scope.row.status === 1 ? 'success' : 'danger'">
                      {{ scope.row.statusText }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="320">
                  <template slot-scope="scope">
                    <el-button size="mini" type="primary" @click="openEditDialog(scope.row)">编辑</el-button>
                    <el-button size="mini" type="danger" @click="handleDelete(scope.row.id)">删除</el-button>
                    <el-button
                        size="mini"
                        :type="scope.row.status === 1 ? 'success' : 'warning'"
                        @click="handleBorrow(scope.row)"
                    >
                      {{ scope.row.status === 1 ? '借书' : '还书' }}
                    </el-button>
                    <el-button size="mini" type="info" @click="showHistory(scope.row)">历史</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </div>

          <!-- 借阅管理页面 -->
          <div v-if="currentMenu === 'borrow'">
            <el-card shadow="never">
              <div style="margin-bottom:15px;">
                <el-input placeholder="输入学号查询借阅记录" v-model="searchUserId" style="width:220px;">
                  <el-button slot="append" icon="el-icon-search" @click="loadBorrowRecords"></el-button>
                </el-input>
                <span style="margin-left:15px;color:#909399;font-size:14px;">借阅记录: {{ borrowRecords.length }} 条</span>
              </div>
              <el-table :data="borrowRecords" border stripe>
                <el-table-column prop="book_name" label="书名" min-width="150"></el-table-column>
                <el-table-column prop="user_id" label="借阅人" width="100"></el-table-column>
                <el-table-column prop="borrow_date" label="借书时间" width="180"></el-table-column>
                <el-table-column prop="return_date" label="还书时间" width="180">
                  <template slot-scope="scope">
                    {{ scope.row.return_date || '未归还' }}
                  </template>
                </el-table-column>
                <el-table-column label="状态" width="100">
                  <template slot-scope="scope">
                    <el-tag :type="scope.row.status === 'borrowed' ? 'danger' : 'success'">
                      {{ scope.row.status === 'borrowed' ? '借出中' : '已归还' }}
                    </el-tag>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </div>
        </el-main>
      </el-container>
    </el-container>

    <!-- 添加/编辑图书弹窗 -->
    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="500px">
      <el-form :model="bookForm" label-width="80px">
        <el-form-item label="书名" required>
          <el-input v-model="bookForm.name" placeholder="请输入书名"></el-input>
        </el-form-item>
        <el-form-item label="作者">
          <el-input v-model="bookForm.author" placeholder="请输入作者"></el-input>
        </el-form-item>
        <el-form-item label="ISBN">
          <el-input v-model="bookForm.isbn" placeholder="请输入ISBN号"></el-input>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="bookForm.status" placeholder="请选择状态">
            <el-option label="在库" :value="1"></el-option>
            <el-option label="已借出" :value="0"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitBook">确定</el-button>
      </span>
    </el-dialog>

    <!-- 借阅历史弹窗 -->
    <el-dialog :title="historyDialogTitle" :visible.sync="historyDialogVisible" width="500px">
      <div v-html="historyContent" style="line-height:1.8;font-size:14px;"></div>
      <span slot="footer">
        <el-button @click="historyDialogVisible = false">确定</el-button>
      </span>
    </el-dialog>

    <!-- 借书弹窗 -->
    <el-dialog title="借书" :visible.sync="borrowDialogVisible" width="400px">
      <div style="text-align:center;padding:20px;">
        <p style="font-size:18px;">📖 {{ currentBook ? currentBook.name : '' }}</p>
        <p style="color:#909399;">请输入学号</p>
        <el-input v-model="borrowUserId" placeholder="请输入学号（如2024001）" style="width:200px;"></el-input>
      </div>
      <span slot="footer">
        <el-button @click="borrowDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmBorrow">确认借书</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      currentMenu: 'books',
      keyword: '',
      books: [],
      borrowRecords: [],
      searchUserId: '',

      dialogVisible: false,
      dialogTitle: '添加图书',
      isEdit: false,
      bookForm: {
        id: null,
        name: '',
        author: '',
        isbn: '',
        status: 1
      },

      borrowDialogVisible: false,
      currentBook: null,
      borrowUserId: '',

      historyDialogVisible: false,
      historyDialogTitle: '',
      historyContent: ''
    }
  },

  mounted() {
    this.loadBooks()
  },

  methods: {
    async loadBooks() {
      try {
        const res = await this.$http.get('/books', {
          params: { keyword: this.keyword }
        })
        if (res.data.code === 200) {
          this.books = res.data.data.map(item => ({
            ...item,
            name: item.bookName,
            status: item.availableCount > 0 ? 1 : 0,
            statusText: item.availableCount > 0 ? '在库' : '已借出'
          }))
        }
      } catch (e) {
        this.$message.error('加载图书失败，请检查后端服务')
      }
    },

    openAddDialog() {
      this.isEdit = false
      this.dialogTitle = '添加图书'
      this.bookForm = { id: null, name: '', author: '', isbn: '', status: 1 }
      this.dialogVisible = true
    },

    openEditDialog(row) {
      this.isEdit = true
      this.dialogTitle = '编辑图书'
      this.bookForm = {
        id: row.id,
        name: row.bookName || row.name,
        author: row.author,
        isbn: row.isbn,
        status: row.availableCount > 0 ? 1 : 0
      }
      this.dialogVisible = true
    },

    async submitBook() {
      if (!this.bookForm.name) {
        this.$message.warning('请输入书名')
        return
      }

      try {
        let res
        if (this.isEdit) {
          res = await this.$http.put(`/books/${this.bookForm.id}`, this.bookForm)
        } else {
          res = await this.$http.post('/books', this.bookForm)
        }
        if (res.data.code === 200) {
          this.$message.success(res.data.message)
          this.dialogVisible = false
          this.loadBooks()
        } else {
          this.$message.error(res.data.message)
        }
      } catch (e) {
        this.$message.error('操作失败')
      }
    },

    async handleDelete(id) {
      const confirm = await this.$confirm('确定要删除这本图书吗？', '提示', {
        type: 'warning'
      }).catch(() => {})
      if (!confirm) return

      try {
        const res = await this.$http.delete(`/books/${id}`)
        if (res.data.code === 200) {
          this.$message.success('删除成功')
          this.loadBooks()
        }
      } catch (e) {
        this.$message.error('删除失败')
      }
    },

    handleBorrow(row) {
      if (row.status === 1) {
        this.currentBook = row
        this.borrowUserId = ''
        this.borrowDialogVisible = true
      } else {
        this.confirmReturn(row.id)
      }
    },

    async confirmBorrow() {
      if (!this.borrowUserId) {
        this.$message.warning('请输入学号')
        return
      }

      try {
        const res = await this.$http.post('/borrows', {
          book_id: this.currentBook.id,
          user_id: parseInt(this.borrowUserId)
        })
        if (res.data.code === 200) {
          this.$message.success('借书成功')
          this.borrowDialogVisible = false
          this.loadBooks()
        } else {
          this.$message.error(res.data.message)
        }
      } catch (e) {
        this.$message.error('借书失败')
      }
    },

    async confirmReturn(bookId) {
      try {
        const res = await this.$http.put('/borrows/return', { book_id: bookId })
        if (res.data.code === 200) {
          this.$message.success('还书成功')
          this.loadBooks()
        } else {
          this.$message.error(res.data.message)
        }
      } catch (e) {
        this.$message.error('还书失败')
      }
    },

    async loadBorrowRecords() {
      if (!this.searchUserId) {
        this.$message.warning('请输入学号查询')
        return
      }

      try {
        const res = await this.$http.get(`/borrows/user/${this.searchUserId}`)
        if (res.data.code === 200) {
          this.borrowRecords = res.data.data
          if (this.borrowRecords.length === 0) {
            this.$message.info('该用户暂无借阅记录')
          }
        }
      } catch (e) {
        this.$message.error('查询失败')
      }
    },

    async showHistory(row) {
      try {
        const res = await this.$http.get(`/borrows/book/${row.id}`)
        if (res.data.code === 200) {
          const history = res.data.data
          if (history.length === 0) {
            this.$message.info('暂无借阅记录')
            return
          }
          const lines = history.map(r => {
            const statusText = r.status === 'borrowed' ? '借出中' : '已归还'
            return `用户${r.user_id} ${r.borrow_date} ${statusText}`
          })
          this.historyDialogTitle = `${row.name} 的借阅历史`
          this.historyContent = lines.join('<br>')
          this.historyDialogVisible = true
        }
      } catch (e) {
        this.$message.error('查询失败')
      }
    },

    handleMenuSelect(index) {
      this.currentMenu = index
      if (index === 'borrow' && this.searchUserId) {
        this.loadBorrowRecords()
      }
    }
  }
}
</script>

<style>
.el-header {
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  position: relative;
  z-index: 10;
}
.el-menu-item i {
  margin-right: 10px;
}
.el-card {
  border-radius: 8px;
}
</style>