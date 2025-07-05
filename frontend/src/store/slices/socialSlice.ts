import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { api } from '../../services/api';

// Interfaces
export interface Post {
  id: number;
  author: {
    id: number;
    username: string;
    email: string;
  };
  content: string;
  post_type: 'text' | 'image' | 'video' | 'race_result' | 'car_update';
  image?: string;
  video?: string;
  likes_count: number;
  comments_count: number;
  is_liked: boolean;
  time_ago: string;
  comments: Array<{
    id: number;
    author: {
      username: string;
    };
    content: string;
    time_ago: string;
  }>;
  created_at: string;
}

export interface Notification {
  id: number;
  sender: {
    username: string;
  };
  notification_type: string;
  title: string;
  message: string;
  is_read: boolean;
  time_ago: string;
  created_at: string;
}

interface SocialState {
  posts: Post[];
  notifications: Notification[];
  activeTab: 'feed' | 'trending';
  filters: {
    postType: string;
    timeFilter: string;
    author: string;
  };
  pagination: {
    page: number;
    hasMore: boolean;
    loading: boolean;
  };
  refreshing: boolean;
  error: string | null;
}

const initialState: SocialState = {
  posts: [],
  notifications: [],
  activeTab: 'feed',
  filters: {
    postType: '',
    timeFilter: '',
    author: '',
  },
  pagination: {
    page: 1,
    hasMore: true,
    loading: false,
  },
  refreshing: false,
  error: null,
};

// Async thunks
export const fetchPosts = createAsyncThunk(
  'social/fetchPosts',
  async ({ page = 1, refresh = false }: { page?: number; refresh?: boolean }, { getState, rejectWithValue }) => {
    try {
      const state = getState() as any;
      const { activeTab, filters } = state.social;
      
      const params = new URLSearchParams({
        page: page.toString(),
        ...(filters.postType && { post_type: filters.postType }),
        ...(filters.timeFilter && { time_filter: filters.timeFilter }),
        ...(filters.author && { author: filters.author }),
      });

      const endpoint = activeTab === 'trending' ? '/api/social/trending/' : '/api/social/feed/';
      const response = await api.get(`${endpoint}?${params}`);
      
      return {
        posts: response.data.results || response.data,
        page,
        refresh,
        hasMore: (response.data.results || response.data).length === 20, // Assuming page size is 20
      };
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch posts');
    }
  }
);

export const fetchNotifications = createAsyncThunk(
  'social/fetchNotifications',
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.get('/api/social/notifications/');
      return response.data.results || response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch notifications');
    }
  }
);

export const createPost = createAsyncThunk(
  'social/createPost',
  async (postData: {
    content: string;
    post_type: 'text' | 'image' | 'video' | 'race_result' | 'car_update';
    image?: File;
    video?: File;
  }, { rejectWithValue }) => {
    try {
      const formData = new FormData();
      formData.append('content', postData.content);
      formData.append('post_type', postData.post_type);
      if (postData.image) {
        formData.append('image', postData.image);
      }
      if (postData.video) {
        formData.append('video', postData.video);
      }

      const response = await api.post('/api/social/posts/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to create post');
    }
  }
);

export const likePost = createAsyncThunk(
  'social/likePost',
  async (postId: number, { getState, rejectWithValue }) => {
    try {
      const state = getState() as any;
      const post = state.social.posts.find((p: Post) => p.id === postId);
      
      if (!post) {
        throw new Error('Post not found');
      }

      const action = post.is_liked ? 'unlike' : 'like';
      await api.post(`/api/social/posts/${postId}/${action}/`);

      return { postId, isLiked: !post.is_liked };
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to like post');
    }
  }
);

export const commentOnPost = createAsyncThunk(
  'social/commentOnPost',
  async ({ postId, content }: { postId: number; content: string }, { rejectWithValue }) => {
    try {
      const response = await api.post(`/api/social/posts/${postId}/comment/`, {
        content
      });

      return { postId, comment: response.data };
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to comment on post');
    }
  }
);

// Social slice
const socialSlice = createSlice({
  name: 'social',
  initialState,
  reducers: {
    setActiveTab: (state, action: PayloadAction<'feed' | 'trending'>) => {
      state.activeTab = action.payload;
      state.pagination.page = 1;
      state.posts = [];
    },
    setPostTypeFilter: (state, action: PayloadAction<string>) => {
      state.filters.postType = action.payload;
      state.pagination.page = 1;
      state.posts = [];
    },
    setTimeFilter: (state, action: PayloadAction<string>) => {
      state.filters.timeFilter = action.payload;
      state.pagination.page = 1;
      state.posts = [];
    },
    setAuthorFilter: (state, action: PayloadAction<string>) => {
      state.filters.author = action.payload;
      state.pagination.page = 1;
      state.posts = [];
    },
    clearFilters: (state) => {
      state.filters = initialState.filters;
      state.pagination.page = 1;
      state.posts = [];
    },
    setRefreshing: (state, action: PayloadAction<boolean>) => {
      state.refreshing = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
    markNotificationRead: (state, action: PayloadAction<number>) => {
      const notification = state.notifications.find(n => n.id === action.payload);
      if (notification) {
        notification.is_read = true;
      }
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch posts
      .addCase(fetchPosts.pending, (state, action) => {
        const { refresh } = action.meta.arg;
        if (refresh) {
          state.refreshing = true;
        } else {
          state.pagination.loading = true;
        }
        state.error = null;
      })
      .addCase(fetchPosts.fulfilled, (state, action) => {
        const { posts, page, refresh, hasMore } = action.payload;
        
        if (refresh || page === 1) {
          state.posts = posts;
        } else {
          state.posts = [...state.posts, ...posts];
        }
        
        state.pagination.page = page;
        state.pagination.hasMore = hasMore;
        state.pagination.loading = false;
        state.refreshing = false;
        state.error = null;
      })
      .addCase(fetchPosts.rejected, (state, action) => {
        state.pagination.loading = false;
        state.refreshing = false;
        state.error = action.payload as string;
      })
      // Fetch notifications
      .addCase(fetchNotifications.fulfilled, (state, action) => {
        state.notifications = action.payload;
      })
      // Create post
      .addCase(createPost.fulfilled, (state, action) => {
        state.posts.unshift(action.payload);
      })
      // Like post
      .addCase(likePost.fulfilled, (state, action) => {
        const { postId, isLiked } = action.payload;
        const post = state.posts.find(p => p.id === postId);
        if (post) {
          post.is_liked = isLiked;
          post.likes_count = isLiked ? post.likes_count + 1 : post.likes_count - 1;
        }
      })
      // Comment on post
      .addCase(commentOnPost.fulfilled, (state, action) => {
        const { postId, comment } = action.payload;
        const post = state.posts.find(p => p.id === postId);
        if (post) {
          post.comments_count += 1;
          post.comments.push(comment);
        }
      });
  },
});

export const {
  setActiveTab,
  setPostTypeFilter,
  setTimeFilter,
  setAuthorFilter,
  clearFilters,
  setRefreshing,
  clearError,
  markNotificationRead,
} = socialSlice.actions;

export default socialSlice.reducer; 