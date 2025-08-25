// اپلیکیشن اصلی سیستم تولید محتوای هوش مصنوعی

class ContentGeneratorApp {
    constructor() {
        this.apiBase = '/api';
        this.currentContent = null;
        this.charts = {};
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadScheduledPosts();
        this.loadStats();
        this.setupCharts();
        this.showToast('سیستم آماده است!', 'success');
    }

    setupEventListeners() {
        // فرم تولید محتوا
        document.getElementById('contentForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.generateContent();
        });

        // فرم زمان‌بندی
        document.getElementById('scheduleForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.scheduleContent();
        });

        // تب‌ها
        document.querySelectorAll('[data-bs-toggle="tab"]').forEach(tab => {
            tab.addEventListener('shown.bs.tab', (e) => {
                const target = e.target.getAttribute('href');
                if (target === '#analytics') {
                    this.refreshStats();
                } else if (target === '#scheduler') {
                    this.loadScheduledPosts();
                }
            });
        });

        // کلیدهای میانبر
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch (e.key) {
                    case 'Enter':
                        e.preventDefault();
                        this.generateContent();
                        break;
                    case 's':
                        e.preventDefault();
                        this.saveContent();
                        break;
                    case 'c':
                        e.preventDefault();
                        this.copyAllContent();
                        break;
                }
            }
        });
    }

    async generateContent() {
        const form = document.getElementById('contentForm');
        const formData = new FormData(form);

        // جمع‌آوری داده‌های فرم
        const topic = formData.get('topic');
        const keywords = formData.get('keywords').split(',').map(k => k.trim()).filter(k => k);
        const audience = formData.get('audience');
        const contentType = formData.get('content_type') || 'post';
        const tone = formData.get('tone') || 'friendly';

        // جمع‌آوری پلتفرم‌های انتخاب شده
        const platforms = [];
        document.querySelectorAll('.platform-checkboxes input:checked').forEach(checkbox => {
            platforms.push(checkbox.value);
        });

        if (!topic.trim()) {
            this.showToast('لطفاً موضوع را وارد کنید', 'error');
            return;
        }

        if (keywords.length === 0) {
            this.showToast('لطفاً حداقل یک کلمه کلیدی وارد کنید', 'error');
            return;
        }

        if (platforms.length === 0) {
            this.showToast('لطفاً حداقل یک پلتفرم انتخاب کنید', 'error');
            return;
        }

        // نمایش لودینگ
        this.showLoading();

        try {
            const response = await fetch(`${this.apiBase}/generate-content`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    topic,
                    keywords,
                    platforms,
                    content_type: contentType,
                    tone,
                    target_audience: audience
                })
            });

            if (!response.ok) {
                throw new Error(`خطای سرور: ${response.status}`);
            }

            const result = await response.json();
            this.currentContent = result;
            this.displayResults(result);
            this.showToast('محتوا با موفقیت تولید شد!', 'success');

        } catch (error) {
            console.error('خطا در تولید محتوا:', error);
            this.showToast(`خطا در تولید محتوا: ${error.message}`, 'error');
        } finally {
            this.hideLoading();
        }
    }

    displayResults(data) {
        const resultsContainer = document.getElementById('results');
        const emptyState = document.getElementById('emptyState');
        const platformResults = document.querySelector('.platform-results');
        const hashtagsContainer = document.querySelector('.hashtags-container');
        const ctaContainer = document.querySelector('.cta-container');

        // پاک کردن نتایج قبلی
        platformResults.innerHTML = '';
        hashtagsContainer.innerHTML = '';
        ctaContainer.innerHTML = '';

        // نمایش نتایج برای هر پلتفرم
        Object.entries(data.contents).forEach(([platform, content]) => {
            const platformDiv = document.createElement('div');
            platformDiv.className = 'platform-result fade-in-up';
            
            const platformIcon = this.getPlatformIcon(platform);
            const platformName = this.getPlatformName(platform);
            
            platformDiv.innerHTML = `
                <div class="d-flex align-items-center mb-3">
                    <div class="platform-icon ${platform}">
                        <i class="${platformIcon}"></i>
                    </div>
                    <div>
                        <h6 class="mb-0">${platformName}</h6>
                        <small class="text-muted">
                            ${content.character_count || 0} کاراکتر • 
                            زمان مطالعه: ${Math.ceil((content.estimated_reading_time || 0) / 60)} دقیقه
                        </small>
                    </div>
                    <div class="ms-auto">
                        <button class="btn btn-sm btn-outline-primary" onclick="app.copyContent('${platform}')">
                            <i class="fas fa-copy"></i>
                        </button>
                    </div>
                </div>
                <div class="content-text" id="content-${platform}">${content.content || content}</div>
            `;
            
            platformResults.appendChild(platformDiv);
        });

        // نمایش هشتگ‌ها
        if (data.hashtags) {
            Object.entries(data.hashtags).forEach(([platform, tags]) => {
                tags.forEach(tag => {
                    const hashtagElement = document.createElement('span');
                    hashtagElement.className = 'hashtag';
                    hashtagElement.textContent = tag;
                    hashtagElement.onclick = () => this.copyText(tag);
                    hashtagsContainer.appendChild(hashtagElement);
                });
            });
        }

        // نمایش پیشنهادات CTA
        if (data.cta_suggestions) {
            data.cta_suggestions.forEach(cta => {
                const ctaElement = document.createElement('div');
                ctaElement.className = 'cta-item';
                ctaElement.innerHTML = `
                    <i class="fas fa-bullhorn me-2 text-primary"></i>
                    ${cta}
                `;
                ctaElement.onclick = () => this.copyText(cta);
                ctaContainer.appendChild(ctaElement);
            });
        }

        // نمایش نتایج و مخفی کردن حالت خالی
        resultsContainer.classList.remove('d-none');
        emptyState.classList.add('d-none');
    }

    getPlatformIcon(platform) {
        const icons = {
            'instagram': 'fab fa-instagram',
            'telegram': 'fab fa-telegram',
            'website': 'fas fa-globe',
            'eitaa': 'fas fa-comments',
            'rubika': 'fas fa-comment-dots'
        };
        return icons[platform] || 'fas fa-share-alt';
    }

    getPlatformName(platform) {
        const names = {
            'instagram': 'اینستاگرام',
            'telegram': 'تلگرام',
            'website': 'وب‌سایت',
            'eitaa': 'ایتا',
            'rubika': 'روبیکا'
        };
        return names[platform] || platform;
    }

    async scheduleContent() {
        const form = document.getElementById('scheduleForm');
        const formData = new FormData(form);

        const platform = formData.get('platform');
        const content = formData.get('content');
        const date = formData.get('date');
        const time = formData.get('time');
        const autoPublish = document.getElementById('autoPublish').checked;

        if (!platform || !content || !date || !time) {
            this.showToast('لطفاً تمام فیلدها را پر کنید', 'error');
            return;
        }

        const scheduleTime = new Date(`${date}T${time}`);
        if (scheduleTime <= new Date()) {
            this.showToast('زمان انتشار باید در آینده باشد', 'error');
            return;
        }

        try {
            const response = await fetch(`${this.apiBase}/schedule-post`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    platform,
                    content,
                    schedule_time: scheduleTime.toISOString(),
                    auto_publish: autoPublish
                })
            });

            if (!response.ok) {
                throw new Error(`خطای سرور: ${response.status}`);
            }

            const result = await response.json();
            this.showToast('محتوا با موفقیت زمان‌بندی شد!', 'success');
            form.reset();
            this.loadScheduledPosts();

        } catch (error) {
            console.error('خطا در زمان‌بندی:', error);
            this.showToast(`خطا در زمان‌بندی: ${error.message}`, 'error');
        }
    }

    async loadScheduledPosts() {
        try {
            const response = await fetch(`${this.apiBase}/scheduled-posts`);
            if (!response.ok) return;

            const posts = await response.json();
            this.displayScheduledPosts(posts);

        } catch (error) {
            console.error('خطا در بارگذاری پست‌های زمان‌بندی شده:', error);
        }
    }

    displayScheduledPosts(posts) {
        const container = document.getElementById('scheduledList');
        container.innerHTML = '';

        if (posts.length === 0) {
            container.innerHTML = `
                <div class="text-center text-muted py-4">
                    <i class="fas fa-calendar fa-2x mb-2"></i>
                    <p>هیچ محتوای زمان‌بندی شده‌ای وجود ندارد</p>
                </div>
            `;
            return;
        }

        posts.forEach(post => {
            const postElement = document.createElement('div');
            postElement.className = 'scheduled-item';
            
            const scheduleDate = new Date(post.schedule_time);
            const isOverdue = scheduleDate < new Date() && post.status === 'scheduled';
            
            postElement.innerHTML = `
                <div class="d-flex justify-content-between align-items-start mb-2">
                    <div>
                        <div class="d-flex align-items-center mb-1">
                            <i class="${this.getPlatformIcon(post.platform)} me-2"></i>
                            <strong>${this.getPlatformName(post.platform)}</strong>
                            <span class="status-badge status-${post.status} ms-2">${this.getStatusText(post.status)}</span>
                            ${isOverdue ? '<span class="badge bg-warning text-dark ms-1">عقب‌افتاده</span>' : ''}
                        </div>
                        <small class="text-muted">
                            <i class="fas fa-clock me-1"></i>
                            ${this.formatDate(scheduleDate)}
                        </small>
                    </div>
                    <div class="btn-group btn-group-sm">
                        ${post.status === 'scheduled' ? `
                            <button class="btn btn-outline-warning" onclick="app.editScheduledPost('${post.id}')">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn btn-outline-danger" onclick="app.cancelScheduledPost('${post.id}')">
                                <i class="fas fa-times"></i>
                            </button>
                        ` : ''}
                    </div>
                </div>
                <div class="content-preview">
                    ${post.content.substring(0, 100)}${post.content.length > 100 ? '...' : ''}
                </div>
            `;
            
            container.appendChild(postElement);
        });
    }

    getStatusText(status) {
        const texts = {
            'scheduled': 'زمان‌بندی شده',
            'published': 'منتشر شده',
            'failed': 'ناموفق',
            'cancelled': 'لغو شده'
        };
        return texts[status] || status;
    }

    formatDate(date) {
        return new Intl.DateTimeFormat('fa-IR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        }).format(date);
    }

    async cancelScheduledPost(id) {
        if (!confirm('آیا از لغو این پست اطمینان دارید؟')) return;

        try {
            const response = await fetch(`${this.apiBase}/scheduled-posts/${id}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error(`خطای سرور: ${response.status}`);
            }

            this.showToast('پست با موفقیت لغو شد', 'success');
            this.loadScheduledPosts();

        } catch (error) {
            console.error('خطا در لغو پست:', error);
            this.showToast(`خطا در لغو پست: ${error.message}`, 'error');
        }
    }

    async loadStats() {
        try {
            const response = await fetch(`${this.apiBase}/stats`);
            if (!response.ok) return;

            const stats = await response.json();
            this.displayStats(stats);

        } catch (error) {
            console.error('خطا در بارگذاری آمار:', error);
        }
    }

    displayStats(stats) {
        document.getElementById('totalGenerated').textContent = stats.total_generated_contents || 0;
        document.getElementById('totalScheduled').textContent = stats.scheduled_posts_count || 0;
        document.getElementById('totalPublished').textContent = '0'; // از API دریافت شود
        document.getElementById('totalViews').textContent = '0'; // از API دریافت شود
    }

    setupCharts() {
        // نمودار عملکرد
        const performanceCtx = document.getElementById('performanceChart').getContext('2d');
        this.charts.performance = new Chart(performanceCtx, {
            type: 'line',
            data: {
                labels: ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه'],
                datasets: [{
                    label: 'محتوای تولید شده',
                    data: [12, 19, 8, 15, 22, 18, 25],
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            font: {
                                family: 'Vazir'
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            font: {
                                family: 'Vazir'
                            }
                        }
                    },
                    x: {
                        ticks: {
                            font: {
                                family: 'Vazir'
                            }
                        }
                    }
                }
            }
        });

        // نمودار پلتفرم‌ها
        const platformCtx = document.getElementById('platformChart').getContext('2d');
        this.charts.platform = new Chart(platformCtx, {
            type: 'doughnut',
            data: {
                labels: ['اینستاگرام', 'تلگرام', 'وب‌سایت', 'ایتا', 'روبیکا'],
                datasets: [{
                    data: [30, 25, 20, 15, 10],
                    backgroundColor: [
                        '#e1306c',
                        '#0088cc',
                        '#10b981',
                        '#06b6d4',
                        '#f59e0b'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            font: {
                                family: 'Vazir'
                            }
                        }
                    }
                }
            }
        });
    }

    async refreshStats() {
        await this.loadStats();
        
        // بروزرسانی نمودارها با داده‌های جدید
        // این بخش را بر اساس API واقعی تکمیل کنید
    }

    copyContent(platform) {
        const contentElement = document.getElementById(`content-${platform}`);
        this.copyText(contentElement.textContent);
    }

    copyAllContent() {
        if (!this.currentContent) return;

        let allContent = '';
        Object.entries(this.currentContent.contents).forEach(([platform, content]) => {
            allContent += `=== ${this.getPlatformName(platform)} ===\n`;
            allContent += (content.content || content) + '\n\n';
        });

        this.copyText(allContent);
    }

    copyText(text) {
        navigator.clipboard.writeText(text).then(() => {
            this.showToast('متن کپی شد!', 'success');
        }).catch(err => {
            console.error('خطا در کپی:', err);
            this.showToast('خطا در کپی متن', 'error');
        });
    }

    saveContent() {
        if (!this.currentContent) return;

        const data = JSON.stringify(this.currentContent, null, 2);
        const blob = new Blob([data], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `content-${Date.now()}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        this.showToast('محتوا ذخیره شد!', 'success');
    }

    async optimizeSEO() {
        if (!this.currentContent) {
            this.showToast('ابتدا محتوایی تولید کنید', 'error');
            return;
        }

        // نمایش مودال SEO
        const modal = new bootstrap.Modal(document.getElementById('seoModal'));
        modal.show();

        // شبیه‌سازی بهینه‌سازی SEO
        document.getElementById('seoResults').innerHTML = `
            <div class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">در حال بهینه‌سازی...</span>
                </div>
                <p class="mt-2">در حال تحلیل و بهینه‌سازی محتوا...</p>
            </div>
        `;

        // شبیه‌سازی تاخیر
        setTimeout(() => {
            document.getElementById('seoResults').innerHTML = `
                <div class="row">
                    <div class="col-md-3 text-center">
                        <div class="seo-score good">85</div>
                        <p class="mt-2">امتیاز SEO</p>
                    </div>
                    <div class="col-md-9">
                        <h6>توصیه‌های بهبود:</h6>
                        <ul class="list-unstyled">
                            <li><i class="fas fa-check text-success me-2"></i>طول محتوا مناسب است</li>
                            <li><i class="fas fa-check text-success me-2"></i>کلمات کلیدی به خوبی توزیع شده‌اند</li>
                            <li><i class="fas fa-exclamation-triangle text-warning me-2"></i>عنوان H1 اضافه کنید</li>
                            <li><i class="fas fa-exclamation-triangle text-warning me-2"></i>متای توضیحات را بهینه کنید</li>
                        </ul>
                    </div>
                </div>
            `;
        }, 2000);
    }

    async generateVisualIdeas() {
        if (!this.currentContent) {
            this.showToast('ابتدا محتوایی تولید کنید', 'error');
            return;
        }

        // نمایش مودال ایده‌های بصری
        const modal = new bootstrap.Modal(document.getElementById('visualModal'));
        modal.show();

        document.getElementById('visualResults').innerHTML = `
            <div class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">در حال تولید ایده‌ها...</span>
                </div>
                <p class="mt-2">در حال تولید ایده‌های بصری خلاقانه...</p>
            </div>
        `;

        // شبیه‌سازی تولید ایده‌ها
        setTimeout(() => {
            document.getElementById('visualResults').innerHTML = `
                <div class="row">
                    <div class="col-md-6">
                        <div class="visual-idea">
                            <h6><i class="fas fa-image me-2"></i>ایده تصویری ۱</h6>
                            <p>طراحی مینیمال با رنگ‌های آبی و سفید، محوریت روی متن اصلی</p>
                            <div class="color-palette">
                                <div class="color-swatch" style="background: #3498db;"></div>
                                <div class="color-swatch" style="background: #ffffff;"></div>
                                <div class="color-swatch" style="background: #f8f9fa;"></div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="visual-idea">
                            <h6><i class="fas fa-video me-2"></i>ایده ویدئویی</h6>
                            <p>انیمیشن کوتاه با موزیک آرام، نمایش مراحل به صورت گام‌به‌گام</p>
                            <small class="text-muted">مدت پیشنهادی: ۳۰ ثانیه</small>
                        </div>
                    </div>
                </div>
                <div class="row mt-3">
                    <div class="col-12">
                        <h6><i class="fas fa-palette me-2"></i>پالت رنگی پیشنهادی</h6>
                        <div class="color-palette">
                            <div class="color-swatch" style="background: #6366f1;"></div>
                            <div class="color-swatch" style="background: #8b5cf6;"></div>
                            <div class="color-swatch" style="background: #06b6d4;"></div>
                            <div class="color-swatch" style="background: #10b981;"></div>
                            <div class="color-swatch" style="background: #f59e0b;"></div>
                        </div>
                    </div>
                </div>
            `;
        }, 2000);
    }

    showLoading() {
        document.getElementById('loadingSpinner').classList.remove('d-none');
        document.getElementById('results').classList.add('d-none');
        document.getElementById('emptyState').classList.add('d-none');
        document.getElementById('generateBtn').disabled = true;
    }

    hideLoading() {
        document.getElementById('loadingSpinner').classList.add('d-none');
        document.getElementById('generateBtn').disabled = false;
    }

    showToast(message, type = 'info') {
        // ایجاد toast برای نمایش پیام‌ها
        const toastContainer = document.getElementById('toastContainer') || this.createToastContainer();
        
        const toastElement = document.createElement('div');
        toastElement.className = `toast align-items-center text-bg-${type === 'error' ? 'danger' : type} border-0`;
        toastElement.setAttribute('role', 'alert');
        toastElement.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-${type === 'success' ? 'check' : type === 'error' ? 'exclamation-triangle' : 'info'} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;

        toastContainer.appendChild(toastElement);
        
        const toast = new bootstrap.Toast(toastElement);
        toast.show();

        // حذف toast پس از نمایش
        toastElement.addEventListener('hidden.bs.toast', () => {
            toastElement.remove();
        });
    }

    createToastContainer() {
        const container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
        return container;
    }
}

// راه‌اندازی اپلیکیشن
const app = new ContentGeneratorApp();

// توابع کمکی برای دسترسی از HTML
window.app = app;
window.copyAllContent = () => app.copyAllContent();
window.saveContent = () => app.saveContent();
window.optimizeSEO = () => app.optimizeSEO();
window.generateVisualIdeas = () => app.generateVisualIdeas();